"""Unit tests for Step 9: Language Selection UI and Persistence."""

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app


class TestLanguageSelectionUIStep9(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.expected_languages = [
            ("en", "English"),
            ("hi", "हिन्दी"),
            ("mr", "मराठी"),
            ("gu", "ગુજરાતી"),
            ("bn", "বাংলা"),
            ("ta", "தமிழ்"),
            ("te", "తెలుగు"),
            ("kn", "ಕನ್ನಡ"),
            ("ml", "മലയാളം"),
            ("pa", "ਪੰਜਾਬੀ"),
        ]

    def test_mobile_locale_provider_native_names_and_persistence(self):
        """Flutter LocaleProvider must include all 10 native script names and SharedPreferences persistence."""
        provider_file = REPO_ROOT / "mobile_app" / "lib" / "providers" / "locale_provider.dart"
        with open(provider_file, mode="r", encoding="utf-8") as f:
            content = f.read()

        for code, native_name in self.expected_languages:
            self.assertIn(f"code: '{code}'", content)
            self.assertIn(f"nativeName: '{native_name}'", content)

        self.assertIn("SharedPreferences.getInstance()", content)
        self.assertIn("selected_language_code", content)

    def test_mobile_home_screen_language_sheet(self):
        """HomeScreen must contain language picker bottom sheet with clear title and native names."""
        home_file = REPO_ROOT / "mobile_app" / "lib" / "screens" / "home_screen.dart"
        with open(home_file, mode="r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Select Language", content)
        self.assertIn("showModalBottomSheet", content)
        self.assertIn("currentLanguage.nativeName", content)

    def test_web_index_html_has_10_language_options(self):
        """Web dashboard navbar must contain all 10 regional options in native script."""
        index_file = REPO_ROOT / "backend" / "app" / "static" / "index.html"
        with open(index_file, mode="r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('id="lang-select"', content)
        for code, native_name in self.expected_languages:
            self.assertIn(f'value="{code}"', content)
            self.assertIn(native_name, content)

    def test_web_app_js_persists_and_translates_all_10_languages(self):
        """Web app.js must have i18n dictionaries for all 10 languages and localStorage persistence."""
        app_js_file = REPO_ROOT / "backend" / "app" / "static" / "app.js"
        with open(app_js_file, mode="r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("localStorage.setItem('aquafootprint_lang'", content)
        self.assertIn("localStorage.getItem('aquafootprint_lang'", content)

        for code, _ in self.expected_languages:
            self.assertIn(f"{code}:", content)

    def test_localized_search_and_scan_e2e(self):
        """End-to-end queries return localized product, comparison, and recommendation."""
        for code, _ in self.expected_languages:
            res = self.client.get(f"/footprint?item=rice&lang={code}")
            self.assertEqual(res.status_code, 200)
            data = res.json()
            self.assertEqual(data["lang"], code)
            self.assertTrue(len(data["item"]) > 0)
            self.assertTrue(len(data["comparison"]) > 0)
            self.assertTrue(len(data["tip"]) > 0)


if __name__ == "__main__":
    unittest.main()
