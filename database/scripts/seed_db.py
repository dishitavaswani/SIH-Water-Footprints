import os
import csv
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.schemas import Base, WaterFootprint, ComparisonReference, AltSuggestions

def seed_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "water_footprint.db")
    csv_path = os.path.join(base_dir, "data", "cleaned_water_footprint.csv")

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Seed WaterFootprint
    items_count = 0
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                wf = WaterFootprint(
                    item_name=row['item_name'].lower().strip(),
                    green_wf=float(row['green_wf']),
                    blue_wf=float(row['blue_wf']),
                    grey_wf=float(row['grey_wf']),
                    unit=row['unit']
                )
                session.add(wf)
                items_count += 1

    # 2. Seed ComparisonReference
    ref_objects = [
        {"object_name": "glass of water", "litres": 0.25},
        {"object_name": "water bottle", "litres": 1.0},
        {"object_name": "toilet flush", "litres": 6.0},
        {"object_name": "bucket", "litres": 15.0},
        {"object_name": "shower", "litres": 65.0},
        {"object_name": "bathtub", "litres": 150.0},
        {"object_name": "swimming pool", "litres": 25000.0}
    ]
    for obj in ref_objects:
        session.add(ComparisonReference(**obj))

    # 3. Seed AltSuggestions
    suggestions = [
        {
            "high_footprint_item": "rice",
            "suggested_alt": "millet / oats",
            "reason": "Millets require significantly less irrigation water to cultivate than rice."
        },
        {
            "high_footprint_item": "beef",
            "suggested_alt": "lentils / beans",
            "reason": "Beef production has an extremely high water footprint compared to plant proteins."
        },
        {
            "high_footprint_item": "chicken",
            "suggested_alt": "lentils / dal",
            "reason": "Plant-based proteins have a dramatically lower water footprint."
        },
        {
            "high_footprint_item": "coffee",
            "suggested_alt": "herbal tea / green tea",
            "reason": "Herbal teas require a fraction of the water needed for processing coffee beans."
        },
        {
            "high_footprint_item": "chocolate",
            "suggested_alt": "seasonal local fruits",
            "reason": "Cocoa cultivation is water-intensive compared to local fruits."
        },
        {
            "high_footprint_item": "almonds",
            "suggested_alt": "sunflower seeds / pumpkin seeds",
            "reason": "Almonds require high irrigation water compared to seed alternatives."
        },
        {
            "high_footprint_item": "cheese",
            "suggested_alt": "tofu / plant-based cheese",
            "reason": "Dairy cheese requires large amounts of water for livestock feed."
        }
    ]
    for sug in suggestions:
        session.add(AltSuggestions(**sug))

    session.commit()
    session.close()
    print(f"Database seeded successfully at: {db_path} ({items_count} items loaded)")

if __name__ == '__main__':
    seed_db()
