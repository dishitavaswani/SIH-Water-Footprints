# 💧 Database & Data Curation Pillar

**Module Owner:** Dishita Vaswani  
**Branch:** `feature/database`  
**Database Target:** SQLite (`database/data/water_footprint.db`)  
**Cleaned Dataset:** CSV (`database/data/cleaned_water_footprint.csv`)

---

## 📌 1. Overview & Architecture

The Database Pillar provides deterministic, standardized, and verified agricultural and dietary water footprint data for the **SIH Water Footprints** application. It delivers:
1. **Deterministic Cleaning Pipeline** from raw heterogeneous data to standardized metric units ($L/\text{kg}$).
2. **Relational SQLite Storage & SQLAlchemy Schemas** with indexed lookups for fast API responses.
3. **Relatable Benchmark Comparisons** (e.g., bathtubs, buckets, standard bottles) and actionable sustainability alternatives.
4. **Standalone Coverage Audit Harness** ensuring 100% alignment with Kuhu's ML computer vision recognition classes and common Food-101 labels.
5. **Clean Integration Layer** in `database/lookup.py` for Aryaveer's FastAPI backend and Shaurya's Flutter mobile app.

```
database/
├── data/
│   ├── raw_water_footprint.csv       # Raw source data with mixed units and headers
│   ├── cleaned_water_footprint.csv   # Normalized, deduplicated dataset in litres/kg
│   └── water_footprint.db            # Seeded SQLite production database
├── models/
│   ├── __init__.py
│   └── schemas.py                    # SQLAlchemy ORM model definitions
├── scripts/
│   ├── clean_dataset.py              # Automated unit conversion & cleaning script
│   ├── seed_db.py                    # Idempotent database creation and seeding script
│   └── audit_coverage.py             # ML model label coverage audit tool
├── lookup.py                         # Backend integration helper methods
├── test_all_items.py                 # Multi-item verification test harness
└── test_dynamic_search.py            # Dynamic SQL query demonstration
```

---

## 🔬 2. Data Provenance & Scientific Methodology

### Data Sources
Data values are sourced from the **Water Footprint Network (WFN)** global assessments and peer-reviewed benchmark literature:
- **Mekonnen, M.M. and Hoekstra, A.Y. (2011)**: *The green, blue and grey water footprint of crops and derived crop products*, Hydrology and Earth System Sciences, 15, 1577-1600.
- **Mekonnen, M.M. and Hoekstra, A.Y. (2012)**: *A Global Assessment of the Water Footprint of Farm Animal Products*, Ecosystems, 15, 401-415.
- **ISO 14046**: *Environmental management — Water footprint — Principles, requirements and guidelines*.

### Water Footprint Component Definitions

$$\text{Total Water Footprint} = \text{Green Water} + \text{Blue Water} + \text{Grey Water}$$

| Component | Description | Relevance & Context |
| :--- | :--- | :--- |
| **🟢 Green Water** | Volume of rainwater consumed during the crop growth period (evaporated or incorporated into biomass). | Critical for rainfed agriculture and soil moisture balance. |
| **🔵 Blue Water** | Volume of surface or groundwater consumed (evaporated, incorporated, or transferred) through artificial irrigation. | Reflects stress on local freshwater aquifers, rivers, and lakes. |
| **⚪ Grey Water** | Volume of freshwater required to assimilate and dilute pollutants (fertilizers, pesticides, wastewater) to reach baseline water quality standards. | Measures the environmental pollution burden of agricultural runoff. |

### Unit Standardization & Conversion Table

All input metrics are converted deterministically to **$\text{litres/kg}$** ($\text{L/kg}$):
- $1\text{ m}^3/\text{tonne} = \frac{1000\text{ L}}{1000\text{ kg}} = 1.0\text{ L/kg}$
- $1\text{ m}^3/\text{ton} = 1.0\text{ L/kg}$
- $1\text{ mL/g} = \frac{0.001\text{ L}}{0.001\text{ kg}} = 1.0\text{ L/kg}$
- $1\text{ US gal/lb} = \frac{3.78541\text{ L}}{0.453592\text{ kg}} \approx 8.3454\text{ L/kg}$

---

## 🗄️ 3. Database Schema & Data Dictionary

### Table: `water_footprint`
Stores primary agricultural and composite food footprint data.

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTOINCREMENT` | Unique record identifier |
| `item_name` | `TEXT` / `VARCHAR` | `UNIQUE`, `NOT NULL`, `INDEXED` | Lowercase standardized item name (e.g., `"rice"`, `"beef"`) |
| `green_wf` | `REAL` / `FLOAT` | `NOT NULL` | Green water footprint in $\text{L/kg}$ |
| `blue_wf` | `REAL` / `FLOAT` | `NOT NULL` | Blue water footprint in $\text{L/kg}$ |
| `grey_wf` | `REAL` / `FLOAT` | `NOT NULL` | Grey water footprint in $\text{L/kg}$ |
| `unit` | `TEXT` / `VARCHAR` | `NOT NULL`, `DEFAULT 'litres/kg'` | Measurement unit (always `litres/kg`) |

### Table: `comparison_reference`
Stores intuitive everyday benchmark volumes for whole-number user comparisons.

| Column | Type | Constraints | Example Value |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTOINCREMENT` | `1` |
| `object_name` | `TEXT` / `VARCHAR` | `UNIQUE`, `NOT NULL` | `"bathtub"`, `"bucket"`, `"standard water bottle"` |
| `litres` | `REAL` / `FLOAT` | `NOT NULL` | `150.0` (bathtub), `15.0` (bucket), `1.0` (bottle) |

### Table: `alt_suggestions`
Stores actionable, lower-footprint dietary recommendations.

| Column | Type | Constraints | Example Value |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTOINCREMENT` | `1` |
| `high_footprint_item` | `TEXT` / `VARCHAR` | `UNIQUE`, `NOT NULL`, `INDEXED` | `"beef"` |
| `suggested_alt` | `TEXT` / `VARCHAR` | `NOT NULL` | `"chicken / lentils / beans"` |
| `reason` | `TEXT` | `NOT NULL` | `"Beef production has an extremely high water footprint compared to plant proteins."` |

---

## 🚀 4. CLI Execution Commands

Run all pipeline scripts from the repository root:

```bash
# 1. Clean raw CSV data into standardized cleaned_water_footprint.csv
python database/scripts/clean_dataset.py

# 2. Create SQLite tables and idempotently seed the database
python database/scripts/seed_db.py

# 3. Audit ML model food label coverage against the database
python database/scripts/audit_coverage.py

# 4. Run automated test suites across all food items
python database/test_all_items.py
python database/test_dynamic_search.py
```

---

## 💻 5. Backend FastAPI Integration Guide

Aryaveer's FastAPI backend (`backend/app/api/endpoints.py`) can import helper functions directly from `database.lookup`:

```python
from database.lookup import get_footprint_data, get_comparison, get_tip

# Example 1: Full structured footprint query (Used by GET /footprint/{item_name})
data = get_footprint_data("rice")
if data:
    print(data)
    # Output:
    # {
    #     "item_name": "rice",
    #     "green_wf": 1200.0,
    #     "blue_wf": 300.0,
    #     "grey_wf": 100.0,
    #     "unit": "litres/kg",
    #     "comparison": "equivalent to ~11 bathtubs of water",
    #     "tip": "Consider replacing with millets / oats for lower water consumption (Millets and oats require significantly less irrigation water to cultivate than flooded rice paddies.)."
    # }
else:
    # Item not found -> Return HTTP 404
    pass

# Example 2: Benchmark comparison for custom total litres
comparison_str = get_comparison(1500.0)
print(comparison_str)
# Output: "equivalent to ~10 bathtubs of water"

# Example 3: Sustainability recommendation tip
tip_str = get_tip("coffee")
print(tip_str)
# Output: "Consider replacing with herbal tea / green tea for lower water consumption..."
```

---

## 📊 6. Coverage & Quality Assurance

- **Total Items in Cleaned Dataset:** 41 distinct agricultural and composite food products.
- **ML Recognition Coverage:** **100.0%** (43 / 43 tested labels including Food-101 and 17 MobileNetV2 classes).
- **Mathematical Consistency:** All entries satisfy $Green \ge 0$, $Blue \ge 0$, $Grey \ge 0$, with units strictly normalized to `litres/kg`.
- **Idempotency:** `seed_db.py` can be executed repeatedly across development environments without generating duplicate entries or constraint violations.
