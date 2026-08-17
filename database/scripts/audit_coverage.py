import os
import sys
import sqlite3
import csv
from typing import List, Optional, Tuple, Dict

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Default Food-101 and MobileNetV2 agricultural recognition labels
DEFAULT_EVALUATION_LABELS = [
    # Food-101 demo items
    "apple_pie",
    "pizza",
    "rice",
    "banana",
    "chicken_curry",
    "hamburger",
    "french_fries",
    "fried_rice",
    "omelette",
    "steak",
    # 17-class agricultural products from ML model
    "almond",
    "cherry",
    "chilli",
    "coconut",
    "cucumber",
    "jowar",
    "lemon",
    "maize",
    "makhana",
    "papaya",
    "pearl_millet",
    "pineapple",
    "sugarcane",
    "tomato",
    "wheat",
    # Common household dietary staples
    "apple",
    "beef",
    "bread",
    "butter",
    "cheese",
    "chicken",
    "chocolate",
    "coffee",
    "corn",
    "eggs",
    "milk",
    "orange",
    "pork",
    "potato",
    "pulses",
    "soybeans",
    "sugar",
    "tea"
]

# Alias and ingredient mapping for composite dishes
FOOD_ALIAS_MAP = {
    "apple_pie": ["apple_pie", "apple"],
    "pizza": ["pizza", "cheese", "wheat", "tomato"],
    "chicken_curry": ["chicken_curry", "chicken"],
    "hamburger": ["hamburger", "beef", "bread"],
    "french_fries": ["french_fries", "potato"],
    "fried_rice": ["fried_rice", "rice"],
    "steak": ["steak", "beef"],
    "omelette": ["omelette", "eggs"],
    "maize": ["maize", "corn"],
    "almond": ["almond", "almonds"],
    "sugarcane": ["sugarcane", "sugar"],
    "pearl_millet": ["pearl_millet", "pulses", "jowar"]
}

def load_database_records(db_path: str = None, csv_path: str = None) -> Dict[str, Dict]:
    """Loads footprint items from SQLite database or fallback cleaned CSV."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if db_path is None:
        db_path = os.path.join(base_dir, "data", "water_footprint.db")
        if not os.path.exists(db_path):
            legacy_path = os.path.join(base_dir, "water_footprint.db")
            if os.path.exists(legacy_path):
                db_path = legacy_path

    if csv_path is None:
        csv_path = os.path.join(base_dir, "data", "cleaned_water_footprint.csv")

    records = {}

    # 1. Try loading from SQLite database
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT item_name, green_wf, blue_wf, grey_wf, unit FROM water_footprint;")
            for row in cursor.fetchall():
                name = row[0].lower().strip()
                records[name] = {
                    "item_name": name,
                    "green_wf": float(row[1]),
                    "blue_wf": float(row[2]),
                    "grey_wf": float(row[3]),
                    "total_wf": float(row[1]) + float(row[2]) + float(row[3]),
                    "unit": row[4]
                }
            conn.close()
            if records:
                return records
        except Exception:
            pass

    # 2. Fallback to cleaned CSV file
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row['item_name'].lower().strip()
                g = float(row['green_wf'])
                b = float(row['blue_wf'])
                gr = float(row['grey_wf'])
                records[name] = {
                    "item_name": name,
                    "green_wf": g,
                    "blue_wf": b,
                    "grey_wf": gr,
                    "total_wf": g + b + gr,
                    "unit": row.get('unit', 'litres/kg')
                }

    return records

def match_label(label: str, db_records: Dict[str, Dict]) -> Tuple[str, Optional[Dict]]:
    """
    Evaluates label matching:
    Returns (status, matched_record)
    Status: 'EXACT', 'FUZZY', or 'MISSING'
    """
    clean_label = label.lower().strip()
    norm_label = clean_label.replace("_", " ")

    # 1. Direct exact match
    if clean_label in db_records:
        return "EXACT", db_records[clean_label]

    if norm_label in db_records:
        return "EXACT", db_records[norm_label]

    # 2. Alias / composite food mapping
    if clean_label in FOOD_ALIAS_MAP:
        for candidate in FOOD_ALIAS_MAP[clean_label]:
            if candidate in db_records:
                return "FUZZY", db_records[candidate]

    # 3. Substring & Fuzzy match
    for item_key, record in db_records.items():
        if item_key in clean_label or item_key in norm_label:
            return "FUZZY", record
        if clean_label in item_key or norm_label in item_key:
            return "FUZZY", record

    return "MISSING", None

def audit_coverage(labels: Optional[List[str]] = None) -> float:
    """
    Audits coverage of ML recognition labels against the database.
    Prints formatted coverage report table and returns coverage percentage.
    """
    eval_labels = labels or DEFAULT_EVALUATION_LABELS
    db_records = load_database_records()

    print("\n" + "=" * 80)
    print(" WATER FOOTPRINT DATABASE COVERAGE AUDIT (Food-101 & ML Recognition)")
    print("=" * 80)
    print(f" Total Database Records Loaded: {len(db_records)}")
    print(f" ML Test Labels Evaluated     : {len(eval_labels)}")
    print("-" * 80)
    print(f"{'ML Model Label':<22} {'Match Status':<15} {'Matched DB Item':<18} {'Total Footprint'}")
    print("-" * 80)

    exact_count = 0
    fuzzy_count = 0
    missing_count = 0

    for label in eval_labels:
        status, match = match_label(label, db_records)

        if status == "EXACT":
            exact_count += 1
            status_display = "✓ EXACT"
            matched_name = match['item_name']
            wf_display = f"{match['total_wf']:>7.0f} {match['unit']}"
        elif status == "FUZZY":
            fuzzy_count += 1
            status_display = "~ FUZZY"
            matched_name = match['item_name']
            wf_display = f"{match['total_wf']:>7.0f} {match['unit']}"
        else:
            missing_count += 1
            status_display = "✗ MISSING"
            matched_name = "-"
            wf_display = "-"

        print(f"{label:<22} {status_display:<15} {matched_name:<18} {wf_display}")

    total = len(eval_labels)
    covered = exact_count + fuzzy_count
    coverage_pct = (covered / total * 100) if total > 0 else 0.0

    print("=" * 80)
    print(f" COVERAGE SUMMARY REPORT:")
    print(f"   • Total Labels Tested : {total}")
    print(f"   • Exact Matches       : {exact_count} ({exact_count / total * 100:.1f}%)")
    print(f"   • Fuzzy/Mapped Matches: {fuzzy_count} ({fuzzy_count / total * 100:.1f}%)")
    print(f"   • Missing Labels      : {missing_count} ({missing_count / total * 100:.1f}%)")
    print(f"   • Overall Coverage    : {coverage_pct:.1f}% ({covered}/{total})")
    print("=" * 80 + "\n")

    return coverage_pct

if __name__ == '__main__':
    # Accept custom labels from CLI arguments if provided
    custom_labels = sys.argv[1:] if len(sys.argv) > 1 else None
    audit_coverage(custom_labels)
