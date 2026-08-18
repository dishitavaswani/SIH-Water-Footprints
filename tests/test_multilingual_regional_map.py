"""Test suite for multilingual support in Crop Suitability & Water Stress Map feature."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app

SUPPORTED_LANGUAGES = ["en", "hi", "mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]

class TestMultilingualRegionalMap(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_regional_detail_multilingual_all_languages(self):
        """Test GET /regional/detail across all 10 supported regional languages."""
        for lang in SUPPORTED_LANGUAGES:
            resp = self.client.get(f"/regional/detail?crop=rice&state=PB&lang={lang}")
            self.assertEqual(resp.status_code, 200, f"Failed for lang: {lang}")
            data = resp.json()

            # Ensure core structure
            self.assertIn("crop", data)
            self.assertIn("region", data)
            self.assertIn("suitability", data)
            self.assertIn("analysis", data)

            crop_name = data["crop"]["name"]
            region_name = data["region"]["name"]
            why_text = data["analysis"]["why_explanation"]

            self.assertTrue(len(crop_name) > 0)
            self.assertTrue(len(region_name) > 0)
            self.assertTrue(len(why_text) > 0)

            print(f" -> Regional Detail Multilingual ({lang}): PASSED")

    def test_marathi_regional_detail(self):
        """Test explicit Marathi localization for Punjab Rice."""
        resp = self.client.get("/regional/detail?crop=rice&state=PB&lang=mr")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        analysis = data["analysis"]
        self.assertIn("analysis", data)
        self.assertTrue(len(analysis["why_explanation"]) > 0)
        print(" -> Marathi Regional Detail (mr): PASSED")

    def test_hindi_regional_detail(self):
        """Test explicit Hindi localization for Punjab Rice."""
        resp = self.client.get("/regional/detail?crop=rice&state=PB&lang=hi")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        analysis = data["analysis"]
        self.assertIn("analysis", data)
        self.assertTrue(len(analysis["why_explanation"]) > 0)
        print(" -> Hindi Regional Detail (hi): PASSED")

if __name__ == "__main__":
    unittest.main()
