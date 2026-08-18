"""Comprehensive Multilingual QA Suite (Steps 1 - 10, Flows A - L, 10 Languages)."""

import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app
from multilingual.registry import get_supported_codes, get_supported_languages
from multilingual.glossary import get_glossary_translation, get_canonical_glossary_terms
from backend.app.services.translation_service import (
    TranslationService,
    BaseTranslationProvider,
    InMemoryCacheProvider,
    SQLiteCacheProvider,
    translate,
)


class MockFailingProvider(BaseTranslationProvider):
    def get_translation(self, text: str, target_lang: str):
        raise TimeoutError("External API Network Timeout")


class FullMultilingualQAPass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.languages = ["en", "hi", "mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]
        cls.test_items = ["rice", "wheat", "apple", "chicken", "coffee", "potato"]

    def _create_sample_image(self) -> io.BytesIO:
        img = Image.new("RGB", (64, 64), color="red")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        return buf

    # ─── Flow A & B & C: Manual Food Search, Footprint, & Breakdown ─────────────
    def test_flow_a_b_c_search_footprint_breakdown_all_languages(self):
        """Flow A, B, C: Tests manual search, footprint retrieval, and water breakdown across all 10 languages."""
        for lang in self.languages:
            for item in self.test_items:
                res = self.client.get(f"/footprint?item={item}&lang={lang}")
                self.assertEqual(res.status_code, 200, f"Failed for item='{item}' lang='{lang}'")
                data = res.json()

                # Language state verification
                self.assertEqual(data["lang"], lang)

                # Unicode string verification (non-empty, no garbage characters or undefined)
                item_display = data["item"]
                self.assertTrue(bool(item_display.strip()), f"Empty item name in {lang}")
                self.assertNotIn("undefined", item_display)
                self.assertNotIn("null", item_display)

                # Numerical metric invariant verification
                total = data["total_litres_per_kg"]
                green = data["green_wf"]
                blue = data["blue_wf"]
                grey = data["grey_wf"]

                self.assertIsInstance(total, (int, float))
                self.assertIsInstance(green, (int, float))
                self.assertIsInstance(blue, (int, float))
                self.assertIsInstance(grey, (int, float))
                self.assertAlmostEqual(total, round(green + blue + grey, 2), places=1)

                # Unit invariant
                self.assertEqual(data["unit"], "litres/kg")

    # ─── Flow D: Comparisons ──────────────────────────────────────────────────
    def test_flow_d_comparisons_all_languages(self):
        """Flow D: Contextual comparison benchmark string localization across all 10 languages."""
        for lang in self.languages:
            res = self.client.get(f"/footprint?item=rice&lang={lang}")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            comp = data.get("comparison", "")
            self.assertTrue(len(comp) > 0, f"Missing comparison for {lang}")
            self.assertNotIn("undefined", comp)
            # Numbers in comparison should be preserved
            self.assertIn("11", comp)

    # ─── Flow E: Sustainability Recommendations ───────────────────────────────
    def test_flow_e_sustainability_recommendations_all_languages(self):
        """Flow E: Sustainability advice localization across all 10 languages."""
        for lang in self.languages:
            res = self.client.get(f"/footprint?item=apple&lang={lang}")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            tip = data.get("tip", "")
            self.assertTrue(len(tip) > 0, f"Missing tip for {lang}")
            self.assertNotIn("undefined", tip)

    # ─── Flow F: Image Scanning ───────────────────────────────────────────────
    def test_flow_f_image_scanning_all_languages(self):
        """Flow F: Image scanning endpoint localization across all 10 languages."""
        for lang in self.languages:
            buf = self._create_sample_image()
            with patch("backend.app.api.endpoints.predict_label", return_value=("apple", 0.94)):
                res = self.client.post(
                    f"/scan?lang={lang}",
                    files={"file": ("apple.jpg", buf, "image/jpeg")},
                )
                self.assertEqual(res.status_code, 200, f"Scan failed for {lang}")
                data = res.json()
                self.assertTrue(data["success"])
                self.assertEqual(data["lang"], lang)
                self.assertEqual(data["canonical_label"], "apple")
                self.assertAlmostEqual(data["confidence"], 0.94, places=2)
                self.assertEqual(data["total_litres_per_kg"], 820.0)
                self.assertEqual(data["unit"], "litres/kg")

    # ─── Flow G: Low-Confidence Image Recognition ─────────────────────────────
    def test_flow_g_low_confidence_recognition_all_languages(self):
        """Flow G: Low confidence (< 0.60) returns localized advisory message and numeric confidence."""
        for lang in self.languages:
            buf = self._create_sample_image()
            with patch("backend.app.api.endpoints.predict_label", return_value=("apple", 0.42)):
                res = self.client.post(
                    f"/scan?lang={lang}",
                    files={"file": ("blurry.jpg", buf, "image/jpeg")},
                )
                self.assertEqual(res.status_code, 200)
                data = res.json()
                self.assertFalse(data["success"])
                self.assertAlmostEqual(data["confidence"], 0.42, places=2)
                self.assertEqual(data["lang"], lang)
                self.assertTrue(len(data["message"]) > 0)
                self.assertNotIn("undefined", data["message"])

    # ─── Flow H: Error Messages & 404 / 400 ────────────────────────────────────
    def test_flow_h_error_messages_and_validation(self):
        """Flow H: Validates 404 on missing item and 400 on unsupported language."""
        # 404 Item Not Found
        res404 = self.client.get("/footprint?item=non_existent_crop_9999&lang=hi")
        self.assertEqual(res404.status_code, 404)
        self.assertIn("not found", res404.json()["detail"].lower())

        # 400 Unsupported Language
        res400 = self.client.get("/footprint?item=rice&lang=unsupported_klingon")
        self.assertEqual(res400.status_code, 400)
        detail = res400.json()["detail"]
        self.assertIn("Unsupported language 'unsupported_klingon'", detail)

    # ─── Flow I: Language Switching ───────────────────────────────────────────
    def test_flow_i_rapid_language_switching(self):
        """Flow I: Switching languages across consecutive requests maintains independent localized state."""
        sequence = ["en", "hi", "mr", "gu", "bn", "ta", "te", "kn", "ml", "pa", "en"]
        expected_rice_names = {
            "en": "rice",
            "hi": "चावल",
            "mr": "तांदूळ",
            "gu": "ચોખા",
            "bn": "চাল / ভাত",
            "ta": "அரிசி",
            "te": "వరి / బియ్యం",
            "kn": "ಅಕ್ಕಿ / ಅನ್ನ",
            "ml": "അരി / ചോറ്",
            "pa": "ਚੌਲ",
        }
        for lang in sequence:
            res = self.client.get(f"/footprint?item=rice&lang={lang}")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["lang"], lang)
            self.assertEqual(data["item"], expected_rice_names[lang])

    # ─── Flow J: Offline Behavior ─────────────────────────────────────────────
    def test_flow_j_offline_resilience(self):
        """Flow J: Validates zero-network offline functionality."""
        offline_service = TranslationService(engine_provider=MockFailingProvider())
        # Scientific glossary offline
        self.assertEqual(offline_service.translate("Green Water", "hi"), "हरा जल")
        self.assertEqual(offline_service.translate("Green Water", "mr"), "हिरवे पाणी")
        self.assertEqual(offline_service.translate("Green Water", "ta"), "பச்சை நீர்")
        # Canonical fallback offline
        self.assertEqual(offline_service.translate("Uncached Rare Herb", "mr"), "Uncached Rare Herb")

    # ─── Flow K: Cached Translations ──────────────────────────────────────────
    def test_flow_k_cache_persistence_and_reuse(self):
        """Flow K: Cached translations are stored under compound key and reused without retranslation."""
        cache = InMemoryCacheProvider()
        cache.set("Sample Custom Entity", "mr", "नमुना सानुकूल घटक")
        svc = TranslationService(cache_provider=cache, engine_provider=MockFailingProvider())
        self.assertEqual(svc.translate("Sample Custom Entity", "mr"), "नमुना सानुकूल घटक")

    # ─── Flow L: Translation Provider Failure ─────────────────────────────────
    def test_flow_l_provider_outage_fails_safe(self):
        """Flow L: Translation provider timeouts/crashes degrade safely to canonical English without throwing exceptions."""
        failing_svc = TranslationService(engine_provider=MockFailingProvider())
        result = failing_svc.translate("Exotic Fruit XYZ", "ta")
        self.assertEqual(result, "Exotic Fruit XYZ")


if __name__ == "__main__":
    unittest.main()
