import os
import sys
import json

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def qa_check_arb():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    en_path = os.path.join(base_dir, "l10n", "app_en.arb")
    hi_path = os.path.join(base_dir, "l10n", "app_hi.arb")

    if not os.path.exists(en_path) or not os.path.exists(hi_path):
        print("Error: ARB files missing.")
        return False

    with open(en_path, mode='r', encoding='utf-8') as f:
        en_data = json.load(f)

    with open(hi_path, mode='r', encoding='utf-8') as f:
        hi_data = json.load(f)

    # Filter out metadata keys starting with @
    en_keys = {k for k in en_data if not k.startswith("@")}
    hi_keys = {k for k in hi_data if not k.startswith("@")}

    missing_in_hi = en_keys - hi_keys
    extra_in_hi = hi_keys - en_keys

    print("=" * 65)
    print(" ARB LOCALIZATION KEY PARITY QA CHECK")
    print("=" * 65)
    print(f" English Keys Count : {len(en_keys)}")
    print(f" Hindi Keys Count   : {len(hi_keys)}")
    print("-" * 65)

    success = True
    if missing_in_hi:
        print(f"❌ Missing keys in app_hi.arb: {missing_in_hi}")
        success = False

    if extra_in_hi:
        print(f"⚠️ Extra keys in app_hi.arb not in app_en.arb: {extra_in_hi}")
        success = False

    empty_hi_keys = [k for k in hi_keys if not str(hi_data.get(k, "")).strip()]
    if empty_hi_keys:
        print(f"❌ Empty translations in app_hi.arb: {empty_hi_keys}")
        success = False

    if success:
        print("✅ SUCCESS: 100% ARB key parity! All English keys have Hindi translations.")
        for k in sorted(en_keys):
            print(f"  • {k:<18} -> EN: '{en_data[k]}' | HI: '{hi_data.get(k, '')}'")

    print("=" * 65 + "\n")
    return success

if __name__ == '__main__':
    ok = qa_check_arb()
    sys.exit(0 if ok else 1)
