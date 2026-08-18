"""Automated ARB Parity & Integrity Validator for all supported regional languages."""

import os
import sys
import json
import re
from pathlib import Path
from typing import Set, Dict, List

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PLACEHOLDER_REGEX = re.compile(r'\{([a-zA-Z0-9_]+)\}')


def extract_placeholders(text: str) -> Set[str]:
    """Extracts all {placeholder} names from an ARB string."""
    if not isinstance(text, str):
        return set()
    return set(PLACEHOLDER_REGEX.findall(text))


def validate_arb_files() -> bool:
    """Validates 100% key parity, non-empty values, and placeholder consistency
    across all ARB localization files in mobile_app/lib/l10n.
    """
    repo_root = Path(__file__).resolve().parents[2]
    l10n_dir = repo_root / "mobile_app" / "lib" / "l10n"
    en_file = l10n_dir / "app_en.arb"

    if not en_file.exists():
        print(f"❌ Error: Canonical English ARB not found at {en_file}")
        return False

    with open(en_file, mode="r", encoding="utf-8") as f:
        en_data: Dict = json.load(f)

    en_keys = {k for k in en_data if not k.startswith("@")}
    all_passed = True

    print("\n" + "=" * 80)
    print(" MULTILINGUAL ARB LOCALIZATION INTEGRITY & PARITY AUDIT")
    print("=" * 80)
    print(f" Source ARB Reference : {en_file.name} ({len(en_keys)} keys)")
    print("-" * 80)

    target_arb_files = sorted(list(l10n_dir.glob("app_*.arb")))

    for arb_path in target_arb_files:
        lang_code = arb_path.stem.replace("app_", "")
        try:
            with open(arb_path, mode="r", encoding="utf-8") as f:
                data: Dict = json.load(f)
        except Exception as err:
            print(f"❌ [{lang_code}] JSON Parse Error in {arb_path.name}: {err}")
            all_passed = False
            continue

        keys = {k for k in data if not k.startswith("@")}
        missing = en_keys - keys
        extra = keys - en_keys
        empty = [k for k in keys if not str(data.get(k, "")).strip()]

        placeholder_errors = []
        for k in en_keys.intersection(keys):
            en_ph = extract_placeholders(en_data[k])
            tgt_ph = extract_placeholders(data[k])
            if en_ph != tgt_ph:
                placeholder_errors.append(f"{k} (EN={en_ph} vs {lang_code}={tgt_ph})")

        status_flag = "✅ PASS"
        issues = []
        if missing:
            status_flag = "❌ FAIL"
            issues.append(f"Missing {len(missing)} keys: {missing}")
            all_passed = False
        if extra:
            status_flag = "⚠️ WARN"
            issues.append(f"Extra {len(extra)} keys: {extra}")
        if empty:
            status_flag = "❌ FAIL"
            issues.append(f"Empty {len(empty)} keys: {empty}")
            all_passed = False
        if placeholder_errors:
            status_flag = "❌ FAIL"
            issues.append(f"Placeholder mismatch: {placeholder_errors}")
            all_passed = False

        status_str = f"{arb_path.name:<18} [{status_flag}] ({len(keys)} keys)"
        if issues:
            print(f"{status_str}\n   └─ {'; '.join(issues)}")
        else:
            print(f"{status_str}")

    print("=" * 80)
    if all_passed:
        print("🎉 ALL REGIONAL ARB LOCALIZATION FILES PASSED 100% PARITY CHECKS!")
    else:
        print("❌ SOME ARB FILES FAILED VALIDATION CHECKS.")
    print("=" * 80 + "\n")
    return all_passed


if __name__ == "__main__":
    success = validate_arb_files()
    sys.exit(0 if success else 1)
