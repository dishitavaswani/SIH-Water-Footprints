"""Unit tests for Step 8: Multilingual Image Scanning Flow."""

import io
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


class TestImageScanningMultilingualStep8(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def _create_dummy_image(self) -> io.BytesIO:
        img = Image.new("RGB", (64, 64), color="red")
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        return buf

    def test_english_scan(self):
        """1. English scan returns canonical English label, untouched numerical metrics, and English text."""
        buf = self._create_dummy_image()
        with patch("backend.app.api.endpoints.predict_label", return_value=("apple", 0.92)):
            response = self.client.post(
                "/scan?lang=en",
                files={"file": ("apple.jpg", buf, "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["lang"], "en")
            self.assertEqual(data["item"], "apple")
            self.assertEqual(data["canonical_label"], "apple")
            self.assertAlmostEqual(data["confidence"], 0.92, places=2)
            self.assertEqual(data["total_litres_per_kg"], 820.0)
            self.assertEqual(data["green_wf"], 700.0)
            self.assertEqual(data["blue_wf"], 80.0)
            self.assertEqual(data["grey_wf"], 40.0)
            self.assertEqual(data["unit"], "litres/kg")
            self.assertIn("bathtubs of water", data["comparison"])

    def test_hindi_scan(self):
        """2. Hindi scan translates item to 'सेब', comparison to Hindi, but leaves numbers and units uncorrupted."""
        buf = self._create_dummy_image()
        with patch("backend.app.api.endpoints.predict_label", return_value=("apple", 0.88)):
            response = self.client.post(
                "/scan?lang=hi",
                files={"file": ("apple.jpg", buf, "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["lang"], "hi")
            self.assertEqual(data["item"], "सेब")
            self.assertEqual(data["canonical_label"], "apple")
            self.assertAlmostEqual(data["confidence"], 0.88, places=2)
            self.assertEqual(data["total_litres_per_kg"], 820.0)
            self.assertEqual(data["green_wf"], 700.0)
            self.assertEqual(data["blue_wf"], 80.0)
            self.assertEqual(data["grey_wf"], 40.0)
            self.assertEqual(data["unit"], "litres/kg")
            self.assertIn("बाथटब पानी के बराबर", data["comparison"])

    def test_marathi_scan(self):
        """3. Marathi scan translates item to 'सफरचंद', comparison to Marathi, leaving numeric values untouched."""
        buf = self._create_dummy_image()
        with patch("backend.app.api.endpoints.predict_label", return_value=("apple", 0.95)):
            response = self.client.post(
                "/scan?lang=mr",
                files={"file": ("apple.jpg", buf, "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data["success"])
            self.assertEqual(data["lang"], "mr")
            self.assertEqual(data["item"], "सफरचंद")
            self.assertEqual(data["canonical_label"], "apple")
            self.assertAlmostEqual(data["confidence"], 0.95, places=2)
            self.assertEqual(data["total_litres_per_kg"], 820.0)
            self.assertEqual(data["green_wf"], 700.0)
            self.assertEqual(data["blue_wf"], 80.0)
            self.assertEqual(data["grey_wf"], 40.0)
            self.assertEqual(data["unit"], "litres/kg")
            self.assertIn("बाथटब पाण्यासमान", data["comparison"])

    def test_unsupported_language_scan(self):
        """4. Unsupported language returns HTTP 400 Bad Request."""
        buf = self._create_dummy_image()
        response = self.client.post(
            "/scan?lang=unsupported_xyz",
            files={"file": ("apple.jpg", buf, "image/jpeg")},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unsupported language 'unsupported_xyz'", response.json()["detail"])

    def test_low_confidence_ml_prediction(self):
        """5. Low-confidence prediction (< 0.60) returns failure advisory with numerical confidence."""
        buf = self._create_dummy_image()
        with patch("backend.app.api.endpoints.predict_label", return_value=("apple", 0.45)):
            response = self.client.post(
                "/scan?lang=mr",
                files={"file": ("blurry.jpg", buf, "image/jpeg")},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertFalse(data["success"])
            self.assertAlmostEqual(data["confidence"], 0.45, places=2)
            self.assertIn("suggested_label", data)
            self.assertEqual(data["lang"], "mr")


if __name__ == "__main__":
    unittest.main()
