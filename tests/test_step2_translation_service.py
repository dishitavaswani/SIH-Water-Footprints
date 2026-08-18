"""Unit tests for Step 2: Scalable Translation Service & Provider Abstractions."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.services.translation_service import (
    TranslationService,
    VerifiedTranslationProvider,
    InMemoryCacheProvider,
    OfflineTemplateProvider,
    ExternalEngineProvider,
    BaseTranslationProvider,
    translate,
    translate_text,
    get_translation_service,
)


class MockEngineProvider(BaseTranslationProvider):
    """Mock engine to test provider injection."""
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.call_count = 0

    def get_translation(self, text: str, target_lang: str):
        self.call_count += 1
        return self.responses.get((text.strip().lower(), target_lang.lower()))


class TestScalableTranslationService(unittest.TestCase):
    def setUp(self):
        self.service = TranslationService()

    def test_english_canonical_passthrough(self):
        """English source text must return unchanged immediately."""
        self.assertEqual(translate("rice", "en"), "rice")
        self.assertEqual(translate("1,600 L/kg", "en"), "1,600 L/kg")
        self.assertEqual(translate("equivalent to ~10 bathtubs of water", "en"), "equivalent to ~10 bathtubs of water")

    def test_verified_hindi_preservation(self):
        """Existing verified Hindi vocabulary must be perfectly preserved."""
        self.assertEqual(translate("rice", "hi"), "चावल")
        self.assertEqual(translate("wheat", "hi"), "गेहूं")
        self.assertEqual(translate("apple", "hi"), "सेब")
        self.assertEqual(translate("coffee", "hi"), "कॉफ़ी")
        self.assertEqual(translate("banana", "hi"), "केला")

    def test_caching_behavior(self):
        """Translations must be cached after first lookup."""
        cache = InMemoryCacheProvider()
        mock_engine = MockEngineProvider({("custom_query", "mr"): "सानुकूल क्वेरी"})
        
        service = TranslationService(
            cache_provider=cache,
            verified_provider=VerifiedTranslationProvider(),
            engine_provider=mock_engine,
            template_provider=OfflineTemplateProvider()
        )
        
        # First call: hits mock engine
        res1 = service.translate("custom_query", "mr")
        self.assertEqual(res1, "सानुकूल क्वेरी")
        self.assertEqual(mock_engine.call_count, 1)

        # Second call: hits cache, mock engine not called again
        res2 = service.translate("custom_query", "mr")
        self.assertEqual(res2, "सानुकूल क्वेरी")
        self.assertEqual(mock_engine.call_count, 1)

    def test_priority_order_verified_over_engine(self):
        """Verified translations must take priority over external engine translations."""
        mock_engine = MockEngineProvider({("rice", "hi"): "गलत अनुवाद"})  # Machine translation
        service = TranslationService(engine_provider=mock_engine)
        
        # 'rice' is verified in verified_hi_overrides.json as 'चावल'
        result = service.translate("rice", "hi")
        self.assertEqual(result, "चावल")
        self.assertEqual(mock_engine.call_count, 0)

    def test_regional_language_translations(self):
        """Regional language vocabulary must be available via offline template provider."""
        self.assertEqual(translate("rice", "mr"), "तांदूळ")
        self.assertEqual(translate("rice", "gu"), "ચોખા")
        self.assertEqual(translate("rice", "ta"), "அரிசி")
        self.assertEqual(translate("rice", "te"), "వరి / బియ్యం")
        self.assertEqual(translate("rice", "kn"), "ಅಕ್ಕಿ / ಅನ್ನ")
        self.assertEqual(translate("rice", "ml"), "അരി / ചോറ്")
        self.assertEqual(translate("rice", "pa"), "ਚੌਲ")
        self.assertEqual(translate("rice", "bn"), "চাল / ভাত")

    def test_benchmark_template_with_numbers(self):
        """Comparison benchmark sentence must preserve numerical counts across languages."""
        phrase = "equivalent to ~15 bathtubs of water"
        
        hi_res = translate(phrase, "hi")
        self.assertIn("15", hi_res)
        self.assertEqual(hi_res, "लगभग 15 बाथटब पानी के बराबर")

        mr_res = translate(phrase, "mr")
        self.assertIn("15", mr_res)
        self.assertEqual(mr_res, "सुमारे 15 बाथटब पाण्यासमान")

        gu_res = translate(phrase, "gu")
        self.assertIn("15", gu_res)
        self.assertEqual(gu_res, "આશરે 15 બાથટબ પાણી બરાબર")

    def test_graceful_english_fallback_no_crash(self):
        """Unknown phrases must fall back to English without raising exceptions."""
        unknown = "Hyper-exotic agricultural commodity XYZ"
        self.assertEqual(translate(unknown, "hi"), unknown)
        self.assertEqual(translate(unknown, "mr"), unknown)
        self.assertEqual(translate(unknown, "ta"), unknown)

    def test_empty_and_none_safety(self):
        """Empty or None values should return empty strings safely."""
        self.assertEqual(translate("", "hi"), "")
        self.assertEqual(translate(None, "hi"), "")
        self.assertEqual(translate_text("", "en"), "")

    def test_backward_compatibility_wrapper(self):
        """translate_text() wrapper must function identically to translate()."""
        self.assertEqual(translate_text("rice", "hi"), "चावल")
        self.assertEqual(translate_text("rice", "en"), "rice")


if __name__ == "__main__":
    unittest.main()
