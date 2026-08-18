"""Unit tests for Step 6: Structured Translation Caching."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.services.translation_service import (
    TranslationService,
    BaseTranslationProvider,
    BaseCacheProvider,
    InMemoryCacheProvider,
    SQLiteCacheProvider,
    HybridCacheProvider,
    format_cache_key,
)


class CountingMockProvider(BaseTranslationProvider):
    def __init__(self, translations=None):
        self.translations = translations or {}
        self.call_count = 0

    def get_translation(self, text: str, target_lang: str):
        self.call_count += 1
        return self.translations.get((text.strip().lower(), target_lang.lower()))


class BrokenCacheProvider(BaseCacheProvider):
    """Simulates a broken or crashing cache infrastructure."""
    def get(self, text: str, target_lang: str, source_lang: str = "en"):
        raise RuntimeError("Simulated Cache Read Outage")

    def set(self, text: str, target_lang: str, translation: str, source_lang: str = "en"):
        raise RuntimeError("Simulated Cache Write Outage")

    def clear(self):
        raise RuntimeError("Simulated Cache Clear Outage")


class TestTranslationCacheStep6(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_cache.db"

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_cache_key_format(self):
        """Cache keys must follow 'source_lang|source_text|target_lang'."""
        key = format_cache_key("en", "Rice requires approximately 1600 litres/kg", "mr")
        self.assertEqual(key, "en|Rice requires approximately 1600 litres/kg|mr")

        key2 = format_cache_key("EN ", " Wheat ", "HI ")
        self.assertEqual(key2, "en|Wheat|hi")

    def test_cache_miss_translation_and_cache_hit(self):
        """First request causes a cache miss and calls provider; second request is served from cache without calling provider."""
        engine_mock = CountingMockProvider({("custom phrase", "mr"): "सानुकूल वाक्यांश"})
        cache = InMemoryCacheProvider()

        service = TranslationService(
            cache_provider=cache,
            glossary_provider=CountingMockProvider({}),
            verified_provider=CountingMockProvider({}),
            engine_provider=engine_mock,
            template_provider=CountingMockProvider({}),
        )

        # 1. Initial lookup -> Cache Miss -> Provider called (count = 1)
        res1 = service.translate("custom phrase", "mr")
        self.assertEqual(res1, "सानुकूल वाक्यांश")
        self.assertEqual(engine_mock.call_count, 1)

        # Verify key exists in cache
        expected_key = format_cache_key("en", "custom phrase", "mr")
        self.assertEqual(cache.get("custom phrase", "mr"), "सानुकूल वाक्यांश")

        # 2. Repeated lookup -> Cache Hit -> Provider NOT called (count remains 1)
        res2 = service.translate("custom phrase", "mr")
        self.assertEqual(res2, "सानुकूल वाक्यांश")
        self.assertEqual(engine_mock.call_count, 1)

    def test_verified_translation_takes_priority_over_cached_translation(self):
        """Verified glossary or sentence translations MUST override existing cached entries."""
        cache = InMemoryCacheProvider()
        # Seed cache with an outdated/suboptimal translation
        cache.set("Green Water", "hi", "पुराना कैश अनुवाद")

        # Verified glossary provider contains authoritative translation
        verified_glossary = CountingMockProvider({("green water", "hi"): "हरा जल"})

        service = TranslationService(
            cache_provider=cache,
            glossary_provider=verified_glossary,
            verified_provider=CountingMockProvider({}),
            engine_provider=CountingMockProvider({}),
            template_provider=CountingMockProvider({}),
        )

        res = service.translate("Green Water", "hi")
        self.assertEqual(res, "हरा जल")

    def test_missing_translation_fallback(self):
        """If term is missing from all providers and cache, return source text gracefully."""
        cache = InMemoryCacheProvider()
        service = TranslationService(
            cache_provider=cache,
            glossary_provider=CountingMockProvider({}),
            verified_provider=CountingMockProvider({}),
            engine_provider=CountingMockProvider({}),
            template_provider=CountingMockProvider({}),
        )

        result = service.translate("Unknown Nonexistent Agricultural Item", "mr")
        self.assertEqual(result, "Unknown Nonexistent Agricultural Item")

    def test_sqlite_cache_persistence_and_offline_durability(self):
        """SQLite cache provider persists translations across provider instances."""
        sqlite_cache1 = SQLiteCacheProvider(db_path=self.db_path)
        sqlite_cache1.set("Banana", "mr", "केळी")

        # Create new cache instance pointing to same file
        sqlite_cache2 = SQLiteCacheProvider(db_path=self.db_path)
        cached_val = sqlite_cache2.get("Banana", "mr")
        self.assertEqual(cached_val, "केळी")

    def test_broken_cache_does_not_crash_translation_service(self):
        """Cache failures (e.g. read/write exceptions) must never break translation requests."""
        broken_cache = BrokenCacheProvider()
        engine_mock = CountingMockProvider({("healthy query", "hi"): "स्वस्थ अनुवाद"})

        service = TranslationService(
            cache_provider=broken_cache,
            glossary_provider=CountingMockProvider({}),
            verified_provider=CountingMockProvider({}),
            engine_provider=engine_mock,
            template_provider=CountingMockProvider({}),
        )

        # Service still returns translation without raising exceptions
        res = service.translate("healthy query", "hi")
        self.assertEqual(res, "स्वस्थ अनुवाद")

    def test_do_not_cache_error_responses(self):
        """Error messages and empty strings should never be stored in the cache."""
        cache = InMemoryCacheProvider()
        cache.set("Broken Query", "hi", "Error: 500 API Limit Exceeded")
        cache.set("Failed Query", "hi", "404 Not Found")
        cache.set("Empty Query", "hi", "   ")

        self.assertIsNone(cache.get("Broken Query", "hi"))
        self.assertIsNone(cache.get("Failed Query", "hi"))
        self.assertIsNone(cache.get("Empty Query", "hi"))


if __name__ == "__main__":
    unittest.main()
