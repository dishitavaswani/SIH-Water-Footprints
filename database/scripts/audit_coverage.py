import os
import sys
import sqlite3

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def audit_coverage():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "water_footprint.db")
    if not os.path.exists(db_path):
        legacy_path = os.path.join(base_dir, "water_footprint.db")
        if os.path.exists(legacy_path):
            db_path = legacy_path

    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Run seed_db.py first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT item_name FROM water_footprint;")
    db_items = {row[0].lower().strip() for row in cursor.fetchall()}
    conn.close()

    # Known food items recognized by the ML model
    ml_recognized_labels = [
        "rice", "wheat", "apple", "milk", "chicken",
        "coffee", "potato", "tomato", "banana", "chocolate",
        "beef", "pork", "eggs", "cheese", "bread", "orange", "tea"
    ]

    print("=" * 65)
    print(" Database Coverage Audit vs ML Recognized Food Labels")
    print("=" * 65)

    missing_items = []
    for label in ml_recognized_labels:
        status = "COVERED" if label in db_items else "MISSING"
        print(f"ML Label: {label:<15} | Status: {status}")
        if label not in db_items:
            missing_items.append(label)

    print("-" * 65)
    if missing_items:
        print(f"Warning: Found {len(missing_items)} missing items in DB: {missing_items}")
    else:
        print("SUCCESS: 100% Coverage! All ML recognized food labels exist in Database.\n")

if __name__ == '__main__':
    audit_coverage()
