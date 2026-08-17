# Database + Data Curation Pillar — Owned by Dishita

Branch Name: `feature/database`

## Responsibilities
- Source, clean, and standardize dataset (`data/raw_water_footprint.csv` -> `data/cleaned_water_footprint.csv`)
- SQLAlchemy DB schema (`models/schemas.py`): `WaterFootprint`, `ComparisonReference`, `AltSuggestions`
- Database seeding script (`scripts/seed_db.py`)
- Lookup functions (`lookup.py`): `get_comparison()`, `get_tip()`
- Coverage auditing script (`scripts/audit_coverage.py`)
