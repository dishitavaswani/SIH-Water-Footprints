import os
import sys
import json
import re
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

def qa_check_arb() -> bool:
    """
    Automated ARB Parity & Integrity Validator:
    - Reads both app_en.arb and app_hi.arb
    - Validates 100% key parity (bidirectional)
    - Validates placeholder consistency (e.g. {item}, {unit})
    - Checks for empty or whitespace-only values
    - Prints structured diagnostic table
    - Returns True if all checks pass, False otherwise
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    en_path = os.path.join(base_dir, "l10n", "app_en.arb")
    hi_path = os.path.join(base_dir, "l10n", "app_hi.arb")

    if not os.path.exists(en_path):
        print(f"❌ Error: English ARB not found at {en_path}")
        return False
    if not os.path.exists(hi_path):
        print(f"❌ Error: Hindi ARB not found at {hi_path}")
        return False

    try:
        with open(en_path, mode='r', encoding='utf-8') as f:
            en_data: Dict = json.load(f)
    except Exception as err:
        print(f"❌ JSON Parse Error in app_en.arb: {err}")
        return False

    try:
        with open(hi_path, mode='r', encoding='utf-8') as f:
            hi_data: Dict = json.load(f)
    except Exception as err:
        print(f"❌ JSON Parse Error in app_hi.arb: {err}")
        return False

    # Extract user keys (ignore metadata keys starting with @ or @@)
    en_keys = {k for k in en_data if not k.startswith("@")}
    hi_keys = {k for k in hi_data if not k.startswith("@")}

    missing_in_hi = en_keys - hi_keys
    extra_in_hi = hi_keys - en_keys
    all_keys = sorted(en_keys | hi_keys)

    print("\n" + "=" * 80)
    print(" ARB LOCALIZATION KEY PARITY & INTEGRITY QA VALIDATOR")
    print("=" * 80)
    print(f" English ARB File : {en_path} ({len(en_keys)} keys)")
    print(f" Hindi ARB File   : {hi_path} ({len(hi_keys)} keys)")
    print("-" * 80)
    print(f"{'Key':<20} {'Status':<12} {'Placeholders':<15} {'English Text'}")
    print("-" * 80)

    has_errors = False
    placeholder_mismatches: List[str] = []
    empty_keys: List[str] = []

    for key in all_keys:
        en_val = en_data.get(key, "")
        hi_val = hi_data.get(key, "")

        key_errors = []

        if key not in en_keys:
            key_errors.append("MISSING_IN_EN")
        if key not in hi_keys:
            key_errors.append("MISSING_IN_HI")

        if not str(en_val).strip() or not str(hi_val).strip():
            key_errors.append("EMPTY_VALUE")
            empty_keys.append(key)

        # Placeholder checks
        en_placeholders = extract_placeholders(en_val)
        hi_placeholders = extract_placeholders(hi_val)

        if en_placeholders != hi_placeholders:
            key_errors.append("PLACEHOLDER_MISMATCH")
            placeholder_mismatches.append(
                f"{key}: EN={en_placeholders} vs HI={hi_placeholders}"
            )

        if key_errors:
            has_errors = True
            status = f"✗ {','.join(key_errors)}"
        else:
            status = "✓ OK"

        p_display = f"{{{','.join(en_placeholders)}}}" if en_placeholders else "-"
        en_display = en_val if len(en_val) <= 28 else en_val[:25] + "..."
        print(f"{key:<20} {status:<12} {p_display:<15} {en_display}")

    print("-" * 80)
    print(" SUMMARY REPORT:")
    print(f"   • Total Keys Evaluated       : {len(all_keys)}")
    print(f"   • Keys Missing in Hindi      : {len(missing_in_hi)}")
    print(f"   • Keys Extra in Hindi        : {len(extra_in_hi)}")
    print(f"   • Empty/Blank Values         : {len(empty_keys)}")
    print(f"   • Placeholder Mismatches     : {len(placeholder_mismatches)}")
    print("=" * 80)

    if has_errors:
        print("\n❌ VALIDATION FAILED:")
        if missing_in_hi:
            print(f"   - Missing in Hindi: {missing_in_hi}")
        if extra_in_hi:
            print(f"   - Extra in Hindi: {extra_in_hi}")
        if empty_keys:
            print(f"   - Empty values: {empty_keys}")
        if placeholder_mismatches:
            print(f"   - Placeholder mismatches: {placeholder_mismatches}")
        print()
        return False

    print("\n✅ VALIDATION PASSED: 100% ARB key parity and placeholder integrity verified.\n")
    return True

if __name__ == '__main__':
    passed = qa_check_arb()
    sys.exit(0 if passed else 1)
