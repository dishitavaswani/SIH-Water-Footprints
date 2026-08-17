import os
import csv
import re

# Unit conversion multipliers to convert values to litres/kg
UNIT_CONVERSION_FACTORS = {
    'litres/kg': 1.0,
    'liter/kg': 1.0,
    'liters/kg': 1.0,
    'l/kg': 1.0,
    'l/kilo': 1.0,
    'm3/ton': 1.0,        # 1 m^3 = 1000 L, 1 ton = 1000 kg => 1000/1000 = 1 L/kg
    'm3/tonne': 1.0,
    'm^3/ton': 1.0,
    'm^3/tonne': 1.0,
    'cubic meters/ton': 1.0,
    'gal/lb': 8.3454,     # 1 US gallon / 1 lb = 3.78541 L / 0.453592 kg ≈ 8.3454 L/kg
    'gallon/lb': 8.3454,
    'gallons/lb': 8.3454,
    'ml/g': 1.0,          # 1 mL / 1 g = 0.001 L / 0.001 kg = 1 L/kg
    'l/g': 1000.0         # 1 L / 1 g = 1000 L/kg
}

def normalize_column_name(col: str) -> str:
    """Normalizes header string by lowercasing and removing punctuation/underscores."""
    return re.sub(r'[^a-z0-9]', '', col.lower())

def find_column_key(row_keys, candidates):
    """Finds matching column name from a list of possible variations."""
    for key in row_keys:
        norm = normalize_column_name(key)
        for cand in candidates:
            if cand in norm:
                return key
    return None

def clean_dataset(raw_path: str = None, cleaned_path: str = None):
    """
    Cleans raw water footprint dataset:
    - Standardizes item names to lowercase and strips whitespace
    - Normalizes mixed units to litres/kg
    - Drops duplicates deterministically
    - Exports to cleaned CSV [item_name, green_wf, blue_wf, grey_wf, unit]
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if raw_path is None:
        raw_path = os.path.join(base_dir, "data", "raw_water_footprint.csv")
    if cleaned_path is None:
        cleaned_path = os.path.join(base_dir, "data", "cleaned_water_footprint.csv")

    if not os.path.exists(raw_path):
        print(f"Error: Raw CSV file not found at {raw_path}")
        return []

    cleaned_records = {}
    total_raw_rows = 0
    duplicate_count = 0
    invalid_rows = 0

    with open(raw_path, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames or []

        item_col = find_column_key(fieldnames, ['product', 'item', 'commodity', 'crop', 'name'])
        green_col = find_column_key(fieldnames, ['green'])
        blue_col = find_column_key(fieldnames, ['blue'])
        grey_col = find_column_key(fieldnames, ['grey', 'gray'])
        unit_col = find_column_key(fieldnames, ['unit'])

        if not all([item_col, green_col, blue_col, grey_col]):
            print(f"Error: Unable to map required columns in {raw_path}. Found headers: {fieldnames}")
            return []

        for row in reader:
            total_raw_rows += 1
            raw_item = row.get(item_col, '')
            if not raw_item:
                invalid_rows += 1
                continue

            item_name = raw_item.strip().lower()

            # Deterministic deduplication: keep first occurrence
            if item_name in cleaned_records:
                duplicate_count += 1
                continue

            try:
                raw_green = float(row.get(green_col, 0))
                raw_blue = float(row.get(blue_col, 0))
                raw_grey = float(row.get(grey_col, 0))
            except (ValueError, TypeError):
                invalid_rows += 1
                continue

            raw_unit = row.get(unit_col, 'litres/kg').strip().lower() if unit_col else 'litres/kg'
            conversion_factor = UNIT_CONVERSION_FACTORS.get(raw_unit, 1.0)

            green_wf = round(raw_green * conversion_factor, 2)
            blue_wf = round(raw_blue * conversion_factor, 2)
            grey_wf = round(raw_grey * conversion_factor, 2)

            cleaned_records[item_name] = {
                'item_name': item_name,
                'green_wf': green_wf,
                'blue_wf': blue_wf,
                'grey_wf': grey_wf,
                'unit': 'litres/kg'
            }

    # Deterministic output: sorted by item_name
    sorted_rows = sorted(cleaned_records.values(), key=lambda r: r['item_name'])

    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    with open(cleaned_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(
            outfile,
            fieldnames=['item_name', 'green_wf', 'blue_wf', 'grey_wf', 'unit']
        )
        writer.writeheader()
        writer.writerows(sorted_rows)

    print("=" * 60)
    print(" DATASET CLEANING SUMMARY")
    print("=" * 60)
    print(f" Raw input file        : {raw_path}")
    print(f" Total rows read       : {total_raw_rows}")
    print(f" Duplicates dropped    : {duplicate_count}")
    print(f" Invalid rows skipped  : {invalid_rows}")
    print(f" Valid unique items    : {len(sorted_rows)}")
    print(f" Exported cleaned CSV  : {cleaned_path}")
    print("=" * 60)

    return sorted_rows

if __name__ == '__main__':
    clean_dataset()
