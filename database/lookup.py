import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models.schemas import WaterFootprint, ComparisonReference, AltSuggestions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "water_footprint.db")

def get_db_session():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    Session = sessionmaker(bind=engine)
    return Session()

def get_water_footprint(item_name: str):
    """
    Queries WaterFootprint table with case-insensitive partial match on item_name.
    """
    if not item_name:
        return None

    session = get_db_session()
    query_str = item_name.strip().lower()
    
    # Direct exact match first
    result = session.query(WaterFootprint).filter(WaterFootprint.item_name == query_str).first()
    
    # Partial match fallback
    if not result:
        result = session.query(WaterFootprint).filter(WaterFootprint.item_name.like(f"%{query_str}%")).first()
        
    session.close()
    
    if result:
        return {
            "item_name": result.item_name,
            "green_wf": result.green_wf,
            "blue_wf": result.blue_wf,
            "grey_wf": result.grey_wf,
            "unit": result.unit
        }
    return None

def get_comparison(litres: float) -> str:
    """
    Picks whichever reference object gives the most intuitive whole-number comparison.
    """
    if litres <= 0:
        return "Negligible water usage"

    session = get_db_session()
    refs = session.query(ComparisonReference).all()
    session.close()

    if not refs:
        num_baths = round(litres / 150.0)
        return f"Equivalent to roughly {num_baths if num_baths > 0 else 1} bathtubs of water"

    best_match = None
    best_diff = float('inf')
    best_count = 1

    for ref in refs:
        count = round(litres / ref.litres)
        if count <= 0:
            count = 1
        diff = abs(litres - (count * ref.litres))
        if diff < best_diff:
            best_diff = diff
            best_match = ref.object_name
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

def get_tip(item_name: str) -> str | None:
    """
    Looks up a suggested lower-footprint alternative.
    """
    if not item_name:
        return None

    session = get_db_session()
    query_str = item_name.strip().lower()
    result = session.query(AltSuggestions).filter(AltSuggestions.high_footprint_item == query_str).first()
    session.close()

    if result:
        return f"Consider replacing with {result.suggested_alt} for lower water consumption ({result.reason})."
    return "Conserve water by choosing locally grown, seasonal produce."

if __name__ == '__main__':
    print("Testing DB Lookup Functions:")
    res = get_water_footprint("rice")
    print("Footprint for 'rice':", res)
    if res:
        total_wf = res['green_wf'] + res['blue_wf'] + res['grey_wf']
        print("Comparison:", get_comparison(total_wf))
        print("Tip:", get_tip("rice"))
