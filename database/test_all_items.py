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

def test_items():
    test_food_items = [
        "apple", "coffee", "chicken", "milk", "wheat",
        "potato", "tomato", "chocolate", "banana", "beef",
        "pork", "cheese", "almonds", "tea", "bread"
    ]

    print("=" * 75)
    print(" Testing Dynamic Database Lookup Across Multiple Food Items")
    print("=" * 75)

    for food in test_food_items:
        data = get_water_footprint(food)
        if data:
            total_wf = data['green_wf'] + data['blue_wf'] + data['grey_wf']
            comparison = get_comparison(total_wf)
            tip = get_tip(food)
            print(f"Item: {food.upper():<10} | Total WF: {total_wf:>7.0f} L/kg | Comparison: {comparison}")
            print(f"            └─ Tip: {tip}\n")
        else:
            print(f"Item: {food:<10} | NOT FOUND IN DB\n")

if __name__ == '__main__':
    test_items()
