import os
import csv

def clean_dataset():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw_water_footprint.csv")
    cleaned_path = os.path.join(base_dir, "data", "cleaned_water_footprint.csv")

    if not os.path.exists(raw_path):
        print(f"Error: Raw CSV not found at {raw_path}")
        return

    cleaned_rows = []
    seen_items = set()

    with open(raw_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            item_name = row['Item'].strip().lower()
            if item_name in seen_items:
                continue
            seen_items.add(item_name)

            try:
                green_wf = float(row['Green_Water'])
                blue_wf = float(row['Blue_Water'])
                grey_wf = float(row['Grey_Water'])
            except ValueError:
                continue

            unit = row['Unit'].strip().lower()
            if unit != 'litres/kg':
                unit = 'litres/kg'

            cleaned_rows.append({
                'item_name': item_name,
                'green_wf': green_wf,
                'blue_wf': blue_wf,
                'grey_wf': grey_wf,
                'unit': unit
            })

    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    with open(cleaned_path, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['item_name', 'green_wf', 'blue_wf', 'grey_wf', 'unit']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Dataset cleaned successfully! {len(cleaned_rows)} items exported to {cleaned_path}")

if __name__ == '__main__':
    clean_dataset()
