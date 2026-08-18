"""Unit tests for Step 3: Verified Agricultural Terminology Glossary System."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from multilingual.glossary import (
    glossary,
    get_glossary_translation,
    get_all_glossary_terms,
    get_canonical_glossary_terms,
)
from backend.app.services.translation_service import (
    TranslationService,
    GlossaryTranslationProvider,
    VerifiedTranslationProvider,
    InMemoryCacheProvider,
    BaseTranslationProvider,
    translate,
)


class MockCustomGlossaryProvider(BaseTranslationProvider):
    def __init__(self, terms=None):
        self.terms = terms or {}
        self.call_count = 0

    def get_translation(self, text: str, target_lang: str):
        self.call_count += 1
        return self.terms.get((text.strip().lower(), target_lang.lower()))


class MockCustomSentenceProvider(BaseTranslationProvider):
    def __init__(self, sentences=None):
        self.sentences = sentences or {}
        self.call_count = 0

    def get_translation(self, text: str, target_lang: str):
        self.call_count += 1
        return self.sentences.get((text.strip().lower(), target_lang.lower()))


class TestAgriculturalGlossaryStep3(unittest.TestCase):
    def setUp(self):
        self.required_canonical_terms = [
            "water footprint",
            "total water footprint",
            "green water",
            "blue water",
            "grey water",
            "rainwater",
            "irrigation",
            "groundwater",
            "surface water",
            "evapotranspiration",
            "agriculture",
            "crop",
            "water consumption",
            "pollution",
            "fertilizer",
            "pesticide",
            "sustainable alternative",
            "water saved",
            "litres per kilogram",
        ]

    def test_canonical_terms_present(self):
        """All required agricultural & scientific terms must be indexed in the canonical index."""
        indexed_terms = get_canonical_glossary_terms()
        for term in self.required_canonical_terms:
            self.assertIn(
                term.lower(),
                indexed_terms,
                f"Missing required canonical term: {term}",
            )

    def test_hindi_verified_scientific_terms(self):
        """Verified Hindi terminology must accurately reflect standard environmental/agricultural science."""
        self.assertEqual(get_glossary_translation("Water Footprint", "hi"), "जल पदचिह्न")
        self.assertEqual(get_glossary_translation("Total Water Footprint", "hi"), "कुल जल पदचिह्न")
        self.assertEqual(get_glossary_translation("Green Water", "hi"), "हरा जल")
        self.assertEqual(get_glossary_translation("Blue Water", "hi"), "नीला जल")
        self.assertEqual(get_glossary_translation("Grey Water", "hi"), "धूसर जल")
        self.assertEqual(get_glossary_translation("Evapotranspiration", "hi"), "वाष्पोत्सर्जन")
        self.assertEqual(get_glossary_translation("Groundwater", "hi"), "भूजल")
        self.assertEqual(get_glossary_translation("Surface Water", "hi"), "सतही जल")
        self.assertEqual(get_glossary_translation("Irrigation", "hi"), "सिंचाई")
        self.assertEqual(get_glossary_translation("Litres per kilogram", "hi"), "लीटर प्रति किलोग्राम")

    def test_regional_verified_scientific_terms(self):
        """Marathi, Gujarati, Tamil, etc. glossary lookups must function cleanly."""
        self.assertEqual(get_glossary_translation("Water Footprint", "mr"), "पाण्याचा ठसा")
        self.assertEqual(get_glossary_translation("Green Water", "mr"), "हिरवे पाणी")
        self.assertEqual(get_glossary_translation("Water Footprint", "ta"), "நீர் தடம்")
        self.assertEqual(get_glossary_translation("Green Water", "ta"), "பச்சை நீர்")
        self.assertEqual(get_glossary_translation("Water Footprint", "te"), "నీటి పాదముద్ర")
        self.assertEqual(get_glossary_translation("Green Water", "te"), "ఆకుపచ్చ నీరు")

    def test_translation_service_priority_glossary_over_sentence(self):
        """Priority 1 (Glossary) must override Priority 2 (Sentence overrides) if a collision occurs."""
        mock_glossary = MockCustomGlossaryProvider({("green water", "hi"): "प्रामाणिक हरा जल"})
        mock_sentence = MockCustomSentenceProvider({("green water", "hi"): "गलत वाक्य अनुवाद"})

        service = TranslationService(
            glossary_provider=mock_glossary,
            verified_provider=mock_sentence,
        )

        result = service.translate("Green Water", "hi")
        self.assertEqual(result, "प्रामाणिक हरा जल")
        self.assertEqual(mock_glossary.call_count, 1)
        self.assertEqual(mock_sentence.call_count, 0)

    def test_translation_service_priority_sentence_when_glossary_misses(self):
        """Priority 2 (Sentence overrides) must be called if term is not in glossary."""
        mock_glossary = MockCustomGlossaryProvider({})
        mock_sentence = MockCustomSentenceProvider({("custom sentence", "hi"): "कस्टम वाक्य"})

        service = TranslationService(
            glossary_provider=mock_glossary,
            verified_provider=mock_sentence,
        )

        result = service.translate("custom sentence", "hi")
        self.assertEqual(result, "कस्टम वाक्य")
        self.assertEqual(mock_glossary.call_count, 1)
        self.assertEqual(mock_sentence.call_count, 1)

    def test_unverified_terms_return_none_safely(self):
        """Non-existent terms must return None from glossary without errors or fake guesses."""
        self.assertIsNone(get_glossary_translation("Unverified Fake Term 123", "hi"))
        self.assertIsNone(get_glossary_translation("Green Water", "unsupported_xyz"))

    def test_e2e_translation_pipeline_with_glossary(self):
        """The global translate() helper must resolve agricultural terms correctly."""
        self.assertEqual(translate("Green Water", "hi"), "हरा जल")
        self.assertEqual(translate("Blue Water", "hi"), "नीला जल")
        self.assertEqual(translate("Grey Water", "hi"), "धूसर जल")
        self.assertEqual(translate("Evapotranspiration", "hi"), "वाष्पोत्सर्जन")


if __name__ == "__main__":
    unittest.main()
