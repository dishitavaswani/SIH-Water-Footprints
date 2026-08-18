"""Verification tests for Step 1: Centralized Language Registry."""

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app
from multilingual.registry import (
    get_supported_codes,
    get_supported_languages,
    is_supported_language,
    normalize_language_code,
)


class TestLanguageRegistryStep1(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.expected_codes = ["en", "hi", "mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]

    def test_registry_codes(self):
        codes = get_supported_codes()
        self.assertEqual(codes, self.expected_codes)

    def test_registry_metadata(self):
        languages = get_supported_languages()
        self.assertEqual(len(languages), 10)
        
        # Verify Hindi is marked as verified
        hi = next(lang for lang in languages if lang["code"] == "hi")
        self.assertTrue(hi["is_verified"])
        self.assertEqual(hi["native_name"], "हिन्दी")

        # Verify other languages are marked with accurate verification status
        mr = next(lang for lang in languages if lang["code"] == "mr")
        self.assertFalse(mr["is_verified"])
        self.assertEqual(mr["native_name"], "मराठी")

    def test_endpoint_get_languages(self):
        response = self.client.get("/languages")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 10)
        self.assertEqual(len(data["languages"]), 10)

    def test_footprint_english_and_hindi(self):
        # English
        r_en = self.client.get("/footprint?item=rice&lang=en")
        self.assertEqual(r_en.status_code, 200)
        self.assertEqual(r_en.json()["item"], "rice")
        self.assertEqual(r_en.json()["lang"], "en")

        # Hindi
        r_hi = self.client.get("/footprint?item=rice&lang=hi")
        self.assertEqual(r_hi.status_code, 200)
        self.assertEqual(r_hi.json()["item"], "चावल")
        self.assertEqual(r_hi.json()["lang"], "hi")

    def test_footprint_other_target_languages(self):
        for code in ["mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]:
            response = self.client.get(f"/footprint?item=rice&lang={code}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["lang"], code)

    def test_unsupported_language_rejection(self):
        for bad_code in ["xyz", "fr", "de", "invalid", "123"]:
            response = self.client.get(f"/footprint?item=rice&lang={bad_code}")
            self.assertEqual(response.status_code, 400)
            detail = response.json().get("detail", "")
            self.assertIn("Unsupported language", detail)
            self.assertIn("en", detail)
            self.assertIn("hi", detail)


if __name__ == "__main__":
    unittest.main()
