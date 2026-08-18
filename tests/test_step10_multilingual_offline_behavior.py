"""Unit tests for Step 10: Multilingual Offline Behavior & Resilience."""

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.translation_service import (
    TranslationService,
    BaseTranslationProvider,
    InMemoryCacheProvider,
    SQLiteCacheProvider,
    translate,
)


class FailingNetworkProvider(BaseTranslationProvider):
    """Simulates zero-internet / DNS failure / timeout."""
    def get_translation(self, text: str, target_lang: str):
        raise ConnectionError("Network is unreachable (Simulated Offline Mode)")


class MalformedResponseProvider(BaseTranslationProvider):
    """Simulates malformed JSON or corrupted external payload."""
    def get_translation(self, text: str, target_lang: str):
        return None


class TestMultilingualOfflineBehaviorStep10(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_english_works_offline(self):
        """1. English must work 100% without network connection."""
        res = self.client.get("/footprint?item=rice&lang=en")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["item"], "rice")
        self.assertEqual(data["lang"], "en")
        self.assertEqual(data["total_litres_per_kg"], 1600.0)

    def test_hindi_verified_translations_work_offline(self):
        """2. Verified Hindi terms (glossary & overrides) must resolve locally without network access."""
        self.assertEqual(translate("rice", "hi"), "चावल")
        self.assertEqual(translate("Green Water", "hi"), "हरा जल")
        self.assertEqual(translate("Blue Water", "hi"), "नीला जल")
        self.assertEqual(translate("Evapotranspiration", "hi"), "वाष्पोत्सर्जन")

    def test_regional_verified_translations_work_offline(self):
        """3. Verified regional vocabulary & agricultural glossary must resolve locally offline."""
        # Marathi
        self.assertEqual(translate("rice", "mr"), "तांदूळ")
        self.assertEqual(translate("Green Water", "mr"), "हिरवे पाणी")
        # Gujarati
        self.assertEqual(translate("rice", "gu"), "ચોખા")
        self.assertEqual(translate("Green Water", "gu"), "લીલું પાણી")
        # Tamil
        self.assertEqual(translate("rice", "ta"), "அரிசி")
        self.assertEqual(translate("Water Footprint", "ta"), "நீர் தடம்")
        # Telugu
        self.assertEqual(translate("Water Footprint", "te"), "నీటి పాదముద్ర")

    def test_cached_translations_work_offline(self):
        """4. Previously cached entries must resolve offline from local cache."""
        cache = InMemoryCacheProvider()
        cache.set("Local Seasonal Crop", "mr", "स्थानिक हंगामी पीक")

        offline_service = TranslationService(
            cache_provider=cache,
            engine_provider=FailingNetworkProvider(),
        )

        res = offline_service.translate("Local Seasonal Crop", "mr")
        self.assertEqual(res, "स्थानिक हंगामी पीक")

    def test_missing_translation_returns_canonical_english_never_blank_or_undefined(self):
        """5. If a translation is unavailable offline, return canonical English text (never blank or undefined)."""
        offline_service = TranslationService(
            engine_provider=FailingNetworkProvider(),
        )

        untranslated_term = "Very Obscure Agricultural Variant XYZ"
        result = offline_service.translate(untranslated_term, "mr")

        self.assertEqual(result, untranslated_term)
        self.assertNotEqual(result, "")
        self.assertNotEqual(result, "undefined")
        self.assertNotEqual(result, "null")
        self.assertIsNotNone(result)

    def test_network_timeout_and_malformed_response_handling(self):
        """6. Graceful handling of network timeouts and malformed responses without throwing exceptions."""
        service_timeout = TranslationService(engine_provider=FailingNetworkProvider())
        service_malformed = TranslationService(engine_provider=MalformedResponseProvider())

        # Never raises exceptions
        res1 = service_timeout.translate("Wheat", "pa")
        self.assertEqual(res1, "ਕਣਕ")  # offline template match

        res2 = service_malformed.translate("Wheat", "pa")
        self.assertEqual(res2, "ਕਣਕ")

    def test_e2e_offline_endpoint_resilience(self):
        """7. FastAPI endpoint /footprint functions without internet access."""
        res = self.client.get("/footprint?item=rice&lang=mr")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["item"], "तांदूळ")
        self.assertEqual(data["total_litres_per_kg"], 1600.0)
        self.assertEqual(data["unit"], "litres/kg")


if __name__ == "__main__":
    unittest.main()
