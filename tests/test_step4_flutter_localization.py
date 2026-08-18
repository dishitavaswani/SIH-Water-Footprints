"""Unit tests for Step 4: Flutter Multilingual Localization Expansion."""

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from multilingual.registry import get_supported_codes, get_supported_languages


class TestFlutterLocalizationStep4(unittest.TestCase):
    def setUp(self):
        self.mobile_l10n_dir = REPO_ROOT / "mobile_app" / "lib" / "l10n"
        self.expected_codes = ["en", "hi", "mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]
        self.expected_native_names = {
            "en": "English",
            "hi": "हिन्दी",
            "mr": "मराठी",
            "gu": "ગુજરાતી",
            "bn": "বাংলা",
            "ta": "தமிழ்",
            "te": "తెలుగు",
            "kn": "ಕನ್ನಡ",
            "ml": "മലയാളം",
            "pa": "ਪੰਜਾਬੀ",
        }

    def test_all_10_arb_files_exist(self):
        """All 10 target ARB files must exist in mobile_app/lib/l10n/."""
        for code in self.expected_codes:
            arb_path = self.mobile_l10n_dir / f"app_{code}.arb"
            self.assertTrue(arb_path.exists(), f"Missing ARB file for {code}: {arb_path}")

    def test_100_percent_key_parity_across_all_arb_files(self):
        """Every ARB file must contain all canonical keys from app_en.arb."""
        en_path = self.mobile_l10n_dir / "app_en.arb"
        with open(en_path, mode="r", encoding="utf-8") as f:
            en_data = json.load(f)
        en_keys = {k for k in en_data if not k.startswith("@")}
        self.assertEqual(len(en_keys), 37, f"Expected 37 keys in app_en.arb, found {len(en_keys)}")

        for code in self.expected_codes:
            arb_path = self.mobile_l10n_dir / f"app_{code}.arb"
            with open(arb_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
            keys = {k for k in data if not k.startswith("@")}
            missing = en_keys - keys
            self.assertEqual(missing, set(), f"Language {code} missing keys: {missing}")

            # Check placeholders {unit} and {item}
            for k in ["allValuesIn", "noDataFound"]:
                en_val = en_data[k]
                tgt_val = data[k]
                en_ph = set(re.findall(r'\{([a-zA-Z0-9_]+)\}', en_val))
                tgt_ph = set(re.findall(r'\{([a-zA-Z0-9_]+)\}', tgt_val))
                self.assertEqual(
                    en_ph,
                    tgt_ph,
                    f"Placeholder mismatch for key '{k}' in {code}: {en_ph} vs {tgt_ph}",
                )

    def test_unverified_languages_have_status_tag(self):
        """Regional languages awaiting human proofreading must be tagged as needs_verification."""
        unverified_codes = ["mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]
        for code in unverified_codes:
            arb_path = self.mobile_l10n_dir / f"app_{code}.arb"
            with open(arb_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(
                data.get("@@x_verification_status"),
                "needs_verification",
                f"Language {code} should have @@x_verification_status = needs_verification",
            )

    def test_app_localizations_dart_contains_all_10_locales(self):
        """mobile_app/lib/l10n/app_localizations.dart must register all 10 locales."""
        dart_path = self.mobile_l10n_dir / "app_localizations.dart"
        with open(dart_path, mode="r", encoding="utf-8") as f:
            content = f.read()

        for code in self.expected_codes:
            self.assertIn(f"Locale('{code}')", content, f"app_localizations.dart missing Locale('{code}')")
            if code != "en":
                cap = code.capitalize()
                self.assertIn(f"_AppLocalizations{cap}", content, f"Missing class _AppLocalizations{cap}")

    def test_locale_provider_native_names(self):
        """LocaleProvider must contain native script names for all 10 languages."""
        provider_path = REPO_ROOT / "mobile_app" / "lib" / "providers" / "locale_provider.dart"
        with open(provider_path, mode="r", encoding="utf-8") as f:
            content = f.read()

        for code, native_name in self.expected_native_names.items():
            self.assertIn(code, content)
            self.assertIn(native_name, content, f"Missing native name '{native_name}' for {code}")


if __name__ == "__main__":
    unittest.main()
