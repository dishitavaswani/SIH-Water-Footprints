"""Unit tests for Step 5: Backend Multilingual API Scaling."""

import io
import sys
import unittest
from pathlib import Path
from PIL import Image
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app


class TestBackendMultilingualAPIStep5(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_footprint_all_supported_languages(self):
        """Endpoints must accept all languages from the registry and return identical numerical metrics."""
        languages = ["en", "hi", "mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]
        
        # Expected translated item names for 'rice'
        expected_items = {
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

        for lang in languages:
            response = self.client.get(f"/footprint?item=rice&lang={lang}")
            self.assertEqual(response.status_code, 200, f"Failed for lang={lang}: {response.text}")
            data = response.json()

            # 1. Validate language tag
            self.assertEqual(data["lang"], lang)

            # 2. Validate human readable item name
            expected_item = expected_items.get(lang)
            if expected_item:
                self.assertEqual(data["item"], expected_item)

            # 3. Validate numerical metrics remain unchanged floats across all languages
            self.assertEqual(data["total_litres_per_kg"], 1600.0)
            self.assertEqual(data["green_wf"], 1200.0)
            self.assertEqual(data["blue_wf"], 300.0)
            self.assertEqual(data["grey_wf"], 100.0)
            self.assertEqual(data["green_water_litres"], 1200.0)
            self.assertEqual(data["blue_water_litres"], 300.0)
            self.assertEqual(data["grey_water_litres"], 100.0)

            # 4. Validate unit is never corrupted
            self.assertEqual(data["unit"], "litres/kg")

    def test_unsupported_language_rejection(self):
        """Unsupported language codes must return HTTP 400 with a clean error message."""
        bad_languages = ["xyz", "fr", "de", "es", "invalid_123"]
        for bad_lang in bad_languages:
            response = self.client.get(f"/footprint?item=rice&lang={bad_lang}")
            self.assertEqual(response.status_code, 400)
            detail = response.json().get("detail", "")
            self.assertIn(f"Unsupported language '{bad_lang}'", detail)
            self.assertIn("en", detail)
            self.assertIn("hi", detail)
            self.assertIn("mr", detail)
            self.assertIn("gu", detail)

    def test_scan_multilingual_response(self):
        """POST /scan must handle all registry languages, translate labels, and preserve numerical confidence & metrics."""
        img = Image.new("RGB", (64, 64), color="green")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        for lang in ["en", "hi", "mr", "gu"]:
            buf.seek(0)
            with patch("backend.app.api.endpoints.predict_label", return_value={"label": "apple", "confidence": 0.95}):
                response = self.client.post(
                    f"/scan?lang={lang}",
                    files={"file": ("apple.jpg", buf, "image/jpeg")},
                )
                self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["lang"], lang)
            self.assertIsInstance(data["confidence"], float)
            self.assertEqual(data["unit"], "litres/kg")
            self.assertIsInstance(data["total_litres_per_kg"], (int, float))

    def test_scan_unsupported_language_rejection(self):
        """POST /scan must also reject unsupported language codes."""
        img = Image.new("RGB", (64, 64), color="blue")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)

        response = self.client.post(
            "/scan?lang=unsupported_xyz",
            files={"file": ("sample.jpg", buf, "image/jpeg")},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported language", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
