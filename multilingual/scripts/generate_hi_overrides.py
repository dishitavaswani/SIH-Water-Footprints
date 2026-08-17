import os
import sys
import json
from typing import Dict

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OVERRIDES_PATH = os.path.join(BASE_DIR, "data", "verified_hi_overrides.json")

def validate_and_format_overrides(file_path: str = OVERRIDES_PATH) -> bool:
    """
    Validates, normalizes (lowercase/trimmed keys), and reformats verified_hi_overrides.json.
    """
    if not os.path.exists(file_path):
        print(f"Error: Overrides file not found at '{file_path}'")
        return False

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except Exception as err:
        print(f"❌ JSON Syntax Error in {file_path}: {err}")
        return False

    if not isinstance(raw_data, dict):
        print(f"❌ Overrides data must be a JSON Object (dict), got {type(raw_data)}")
        return False

    normalized_data: Dict[str, str] = {}
    invalid_entries = 0
    duplicate_count = 0

    for key, value in raw_data.items():
        if not isinstance(key, str) or not isinstance(value, str):
            invalid_entries += 1
            continue

        clean_key = key.strip().lower()
        clean_value = value.strip()

        if not clean_key or not clean_value:
            invalid_entries += 1
            continue

        if clean_key in normalized_data:
            duplicate_count += 1

        normalized_data[clean_key] = clean_value

    # Write back normalized, cleanly formatted JSON
    with open(file_path, mode='w', encoding='utf-8') as f:
        json.dump(normalized_data, f, ensure_ascii=False, indent=2)

    print("=" * 65)
    print(" VERIFIED HINDI OVERRIDES VALIDATION REPORT")
    print("=" * 65)
    print(f" Target File        : {file_path}")
    print(f" Total Valid Keys   : {len(normalized_data)}")
    print(f" Duplicate Keys     : {duplicate_count}")
    print(f" Invalid Entries    : {invalid_entries}")
    print(f" File Status        : ✅ Validated & Formatted Cleanly")
    print("=" * 65)

    return True

if __name__ == '__main__':
    ok = validate_and_format_overrides()
    sys.exit(0 if ok else 1)
