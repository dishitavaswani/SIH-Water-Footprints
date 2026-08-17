import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.lookup import get_water_footprint, get_comparison, get_tip

def test_dynamic_query(search_term: str):
    print(f"\n🔍 Executing SQL Query for search term: '{search_term}'...")
    data = get_water_footprint(search_term)
    
    if data:
        total_wf = data['green_wf'] + data['blue_wf'] + data['grey_wf']
        comparison = get_comparison(total_wf)
        tip = get_tip(data['item_name'])
        print(f"✅ Found in SQLite Table 'water_footprint':")
        print(f"   • Item Name: {data['item_name']}")
        print(f"   • Green Water Footprint: {data['green_wf']} L/kg")
        print(f"   • Blue Water Footprint:  {data['blue_wf']} L/kg")
        print(f"   • Grey Water Footprint:  {data['grey_wf']} L/kg")
        print(f"   • Total Water Footprint: {total_wf} L/kg")
        print(f"   • Dynamic Comparison:    {comparison}")
        print(f"   • Dynamic Alternative:   {tip}")
    else:
        print(f"❌ '{search_term}' not found in SQLite Database (Return HTTP 404).")

if __name__ == '__main__':
    print("=" * 70)
    print(" DYNAMIC SQL DATABASE LOOKUP DEMONSTRATION")
    print("=" * 70)
    
    # Test arbitrary queries
    test_dynamic_query("coffee")
    test_dynamic_query("banana")
    test_dynamic_query("chocolate")
    test_dynamic_query("cheese")
    test_dynamic_query("mango") # Item not in DB -> dynamic 404
