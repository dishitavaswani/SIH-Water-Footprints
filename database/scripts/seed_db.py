import os
import csv
import sys
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from models.schemas import Base, WaterFootprint, ComparisonReference, AltSuggestions, HAS_SQLALCHEMY
except ImportError:
    HAS_SQLALCHEMY = False

def seed_db(db_path: str = None, csv_path: str = None):
    """
    Idempotent seeding script:
    - Creates tables if they do not exist
    - Re-seeds water_footprint records from cleaned_water_footprint.csv
    - Re-seeds benchmark comparison references (bathtub, bucket, standard water bottle)
    - Re-seeds actionable alternative suggestions for high footprint items
    - Safe to run multiple times without duplicating entries
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if db_path is None:
        db_path = os.path.join(base_dir, "data", "water_footprint.db")
    if csv_path is None:
        csv_path = os.path.join(base_dir, "data", "cleaned_water_footprint.csv")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Approved benchmark reference objects
    ref_objects = [
        ("glass of water", 0.25),
        ("standard water bottle", 1.0),
        ("toilet flush", 6.0),
        ("bucket", 15.0),
        ("shower", 65.0),
        ("bathtub", 150.0),
        ("swimming pool", 25000.0)
    ]

    # Alternative suggestions for high-footprint agricultural items
    suggestions = [
        (
            "beef",
            "chicken / lentils / beans",
            "Beef production has an extremely high water footprint compared to plant proteins and poultry."
        ),
        (
            "rice",
            "millets / oats",
            "Millets and oats require significantly less irrigation water to cultivate than flooded rice paddies."
        ),
        (
            "chicken",
            "lentils / dal / tofu",
            "Plant-based proteins have a dramatically lower water footprint than poultry."
        ),
        (
            "coffee",
            "herbal tea / green tea",
            "Herbal teas require a fraction of the water needed for growing and processing coffee beans."
        ),
        (
            "chocolate",
            "seasonal local fruits",
            "Cocoa cultivation and processing is water-intensive compared to local fresh fruits."
        ),
        (
            "almonds",
            "sunflower seeds / pumpkin seeds",
            "Almonds require intensive year-round irrigation compared to seed alternatives."
        ),
        (
            "cheese",
            "tofu / plant-based cheese",
            "Dairy cheese requires large amounts of water for dairy cattle and feed production."
        ),
        (
            "pork",
            "lentils / tofu / chicken",
            "Pork has a higher water footprint than plant-based proteins or poultry."
        ),
        (
            "butter",
            "olive oil / plant-based spreads",
            "Plant-based oils require less lifecycle water than dairy butter."
        )
    ]

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Create Tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS water_footprint (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT UNIQUE NOT NULL,
                green_wf REAL NOT NULL,
                blue_wf REAL NOT NULL,
                grey_wf REAL NOT NULL,
                unit TEXT NOT NULL DEFAULT 'litres/kg'
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_water_footprint_item_name ON water_footprint (item_name);")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comparison_reference (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                object_name TEXT UNIQUE NOT NULL,
                litres REAL NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alt_suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                high_footprint_item TEXT UNIQUE NOT NULL,
                suggested_alt TEXT NOT NULL,
                reason TEXT NOT NULL
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_alt_suggestions_high_footprint_item ON alt_suggestions (high_footprint_item);")

        # Clear existing records for idempotent seeding
        cursor.execute("DELETE FROM water_footprint;")
        cursor.execute("DELETE FROM comparison_reference;")
        cursor.execute("DELETE FROM alt_suggestions;")

        # 2. Seed WaterFootprint from CSV
        items_count = 0
        if os.path.exists(csv_path):
            with open(csv_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute("""
                        INSERT INTO water_footprint (item_name, green_wf, blue_wf, grey_wf, unit)
                        VALUES (?, ?, ?, ?, ?);
                    """, (
                        row['item_name'].lower().strip(),
                        float(row['green_wf']),
                        float(row['blue_wf']),
                        float(row['grey_wf']),
                        row.get('unit', 'litres/kg')
                    ))
                    items_count += 1

        # 3. Seed ComparisonReference
        for obj_name, litres in ref_objects:
            cursor.execute("""
                INSERT INTO comparison_reference (object_name, litres)
                VALUES (?, ?);
            """, (obj_name, litres))

        # 4. Seed AltSuggestions
        for high_item, alt, reason in suggestions:
            cursor.execute("""
                INSERT INTO alt_suggestions (high_footprint_item, suggested_alt, reason)
                VALUES (?, ?, ?);
            """, (high_item, alt, reason))

        conn.commit()

        print("=" * 60)
        print(" DATABASE SEEDING COMPLETE")
        print("=" * 60)
        print(f" Database file         : {db_path}")
        print(f" Seeded WaterFootprint : {items_count} items")
        print(f" Seeded Comparisons    : {len(ref_objects)} benchmark objects")
        print(f" Seeded Alternatives   : {len(suggestions)} suggestions")
        print("=" * 60)

    except Exception as e:
        conn.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        conn.close()

if __name__ == '__main__':
    seed_db()
