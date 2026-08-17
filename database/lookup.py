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
    return sqlite3.connect(DB_PATH)

def get_water_footprint(item_name: str):
    """
    Queries water_footprint table with case-insensitive partial match on item_name.
    """
    if not item_name or not os.path.exists(DB_PATH):
        return None

    query_str = item_name.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Exact match first
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

        if row:
            return {
                "item_name": row[0],
                "green_wf": row[1],
                "blue_wf": row[2],
                "grey_wf": row[3],
                "unit": row[4]
            }
        return None
    finally:
        conn.close()

def get_comparison(litres: float) -> str:
    """
    Picks whichever reference object gives the most intuitive whole-number comparison.
    """
    if litres <= 0:
        return "Negligible water usage"

    if not os.path.exists(DB_PATH):
        num_baths = round(litres / 150.0)
        return f"Equivalent to roughly {num_baths if num_baths > 0 else 1} bathtubs of water"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT object_name, litres FROM comparison_reference;")
        refs = cursor.fetchall()
    finally:
        conn.close()

    if not refs:
        num_baths = round(litres / 150.0)
        return f"Equivalent to roughly {num_baths if num_baths > 0 else 1} bathtubs of water"

    best_match = None
    best_diff = float('inf')
    best_count = 1

    for obj_name, ref_litres in refs:
        count = round(litres / ref_litres)
        if count <= 0:
            count = 1
        diff = abs(litres - (count * ref_litres))
        if diff < best_diff:
            best_diff = diff
            best_match = obj_name
            best_count = count

    plural_map = {
        "glass of water": "glasses of water",
        "water bottle": "water bottles",
        "toilet flush": "toilet flushes",
        "bucket": "buckets",
        "shower": "showers",
        "bathtub": "bathtubs",
        "swimming pool": "swimming pools"
    }

    object_label = plural_map.get(best_match, f"{best_match}s") if best_count > 1 else best_match
    return f"Equivalent to roughly {best_count} {object_label}"

def get_tip(item_name: str) -> str:
    """
    Looks up a suggested lower-footprint alternative.
    """
    if not item_name or not os.path.exists(DB_PATH):
        return "Conserve water by choosing locally grown, seasonal produce."

    query_str = item_name.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT suggested_alt, reason
            FROM alt_suggestions
            WHERE high_footprint_item = ?
            LIMIT 1;
        """, (query_str,))
        row = cursor.fetchone()

        if row:
            return f"Consider replacing with {row[0]} for lower water consumption ({row[1]})."
        return "Conserve water by choosing locally grown, seasonal produce."
    finally:
        conn.close()

if __name__ == '__main__':
    print("Testing DB Lookup Functions:")
    res = get_water_footprint("rice")
    print("Footprint for 'rice':", res)
    if res:
        total_wf = res['green_wf'] + res['blue_wf'] + res['grey_wf']
        print("Comparison:", get_comparison(total_wf))
        print("Tip:", get_tip("rice"))
