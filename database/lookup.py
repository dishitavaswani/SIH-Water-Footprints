import os
import sys
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "water_footprint.db")
if not os.path.exists(DB_PATH):
    legacy_path = os.path.join(BASE_DIR, "water_footprint.db")
    if os.path.exists(legacy_path):
        DB_PATH = legacy_path

def get_connection():
    """Returns a SQLite connection to the water footprint database."""
    return sqlite3.connect(DB_PATH)

def get_comparison(litres: float, db_session=None) -> str:
    """
    Selects the most intuitive whole-number comparison object
    (e.g., 'equivalent to ~10 bathtubs of water').
    """
    if litres is None or litres <= 0:
        return "negligible water footprint"

    refs = []
    # If a SQLAlchemy session or custom session is passed
    if db_session is not None and hasattr(db_session, "query"):
        try:
            from models.schemas import ComparisonReference
            query_res = db_session.query(ComparisonReference).all()
            refs = [(r.object_name, r.litres) for r in query_res]
        except Exception:
            refs = []

    # Fallback to direct SQLite connection
    if not refs and os.path.exists(DB_PATH):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT object_name, litres FROM comparison_reference;")
            refs = cursor.fetchall()
            conn.close()
        except Exception:
            refs = []

    # Default fallback benchmarks if DB not yet seeded
    if not refs:
        refs = [
            ("standard water bottle", 1.0),
            ("bucket", 15.0),
            ("shower", 65.0),
            ("bathtub", 150.0),
            ("swimming pool", 25000.0)
        ]

    # Select the reference object that gives the most natural whole-number ratio
    best_match = None
    best_score = float('inf')
    best_count = 1

    for obj_name, ref_litres in refs:
        if ref_litres <= 0:
            continue
        exact_ratio = litres / ref_litres
        count = round(exact_ratio)
        if count <= 0:
            count = 1
        
        # Penalize very large numbers (> 200) or very small fractional numbers
        if count > 200:
            score = count * 10
        elif 1 <= count <= 100:
            # Ideal whole-number range
            score = abs(exact_ratio - count) + (abs(count - 5) * 0.05)
        else:
            score = abs(exact_ratio - count) + 5.0

        if score < best_score:
            best_score = score
            best_match = obj_name
            best_count = count

    if best_match is None:
        best_match = "bathtub"
        best_count = max(1, round(litres / 150.0))

    plural_map = {
        "glass of water": "glasses of water",
        "standard water bottle": "standard water bottles",
        "water bottle": "water bottles",
        "toilet flush": "toilet flushes",
        "bucket": "buckets",
        "shower": "showers",
        "bathtub": "bathtubs",
        "swimming pool": "swimming pools"
    }

    object_label = plural_map.get(best_match, f"{best_match}s") if best_count > 1 else best_match
    return f"equivalent to ~{best_count} {object_label} of water"

def get_tip(item_name: str, db_session=None) -> str | None:
    """
    Queries alt_suggestions for a given item and returns a helpful sustainability tip.
    """
    if not item_name:
        return None

    query_str = item_name.strip().lower()

    # If a SQLAlchemy session is passed
    if db_session is not None and hasattr(db_session, "query"):
        try:
            from models.schemas import AltSuggestions
            record = db_session.query(AltSuggestions).filter(
                AltSuggestions.high_footprint_item == query_str
            ).first()
            if record:
                return f"Consider replacing with {record.suggested_alt} for lower water consumption ({record.reason})."
        except Exception:
            pass

    # Fallback to direct SQLite connection
    if os.path.exists(DB_PATH):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT suggested_alt, reason
                FROM alt_suggestions
                WHERE high_footprint_item = ?
                LIMIT 1;
            """, (query_str,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return f"Consider replacing with {row[0]} for lower water consumption ({row[1]})."
        except Exception:
            pass

    return "Conserve water by choosing locally grown, seasonal produce."

def get_water_footprint(item_name: str, db_session=None) -> dict | None:
    """
    Queries water_footprint table with case-insensitive partial match on item_name.
    """
    if not item_name:
        return None

    query_str = item_name.strip().lower()

    # If a SQLAlchemy session is passed
    if db_session is not None and hasattr(db_session, "query"):
        try:
            from models.schemas import WaterFootprint
            record = db_session.query(WaterFootprint).filter(
                WaterFootprint.item_name == query_str
            ).first()
            if not record:
                record = db_session.query(WaterFootprint).filter(
                    WaterFootprint.item_name.like(f"%{query_str}%")
                ).first()
            if record:
                return {
                    "item_name": record.item_name,
                    "green_wf": record.green_wf,
                    "blue_wf": record.blue_wf,
                    "grey_wf": record.grey_wf,
                    "unit": record.unit
                }
        except Exception:
            pass

    # Fallback to direct SQLite connection
    if os.path.exists(DB_PATH):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Exact match
            cursor.execute("""
                SELECT item_name, green_wf, blue_wf, grey_wf, unit
                FROM water_footprint
                WHERE item_name = ?
                LIMIT 1;
            """, (query_str,))
            row = cursor.fetchone()

            # Partial match fallback
            if not row:
                cursor.execute("""
                    SELECT item_name, green_wf, blue_wf, grey_wf, unit
                    FROM water_footprint
                    WHERE item_name LIKE ?
                    LIMIT 1;
                """, (f"%{query_str}%",))
                row = cursor.fetchone()

            conn.close()

            if row:
                return {
                    "item_name": row[0],
                    "green_wf": row[1],
                    "blue_wf": row[2],
                    "grey_wf": row[3],
                    "unit": row[4]
                }
        except Exception:
            pass

    return None

def get_footprint_data(item_name: str, db_session=None) -> dict | None:
    """
    Queries water_footprint with case-insensitive search and returns:
    {
        item_name,
        green_wf,
        blue_wf,
        grey_wf,
        unit,
        comparison,
        tip
    }
    """
    raw_data = get_water_footprint(item_name, db_session=db_session)
    if not raw_data:
        return None

    total_litres = raw_data["green_wf"] + raw_data["blue_wf"] + raw_data["grey_wf"]
    comparison = get_comparison(total_litres, db_session=db_session)
    tip = get_tip(raw_data["item_name"], db_session=db_session)

    return {
        "item_name": raw_data["item_name"],
        "green_wf": raw_data["green_wf"],
        "blue_wf": raw_data["blue_wf"],
        "grey_wf": raw_data["grey_wf"],
        "unit": raw_data["unit"],
        "comparison": comparison,
        "tip": tip
    }

if __name__ == '__main__':
    print("=" * 60)
    print(" TESTING LOOKUP HELPERS")
    print("=" * 60)
    for test_food in ["rice", "beef", "apple", "coffee", "banana"]:
        data = get_footprint_data(test_food)
        print(f"\nFood Item: {test_food.upper()}")
        if data:
            print(f"  • Green WF   : {data['green_wf']} {data['unit']}")
            print(f"  • Blue WF    : {data['blue_wf']} {data['unit']}")
            print(f"  • Grey WF    : {data['grey_wf']} {data['unit']}")
            print(f"  • Comparison : {data['comparison']}")
            print(f"  • Tip        : {data['tip']}")
        else:
            print("  • NOT FOUND")
