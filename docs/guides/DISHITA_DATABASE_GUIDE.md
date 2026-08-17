# Dishita — Database and Data Guide

## Your ownership

You own data curation and database logic on `feature/database`.

Work only in `database/` unless the team agrees that a shared contract must change.

| File or folder | Your responsibility |
| --- | --- |
| `database/data/` | raw and cleaned water-footprint data |
| `database/models/schemas.py` | data/database schemas |
| `database/scripts/clean_dataset.py` | unit normalization and cleaning |
| `database/scripts/seed_db.py` | database creation and seeding |
| `database/scripts/audit_coverage.py` | model-label coverage checks |
| `database/lookup.py` | comparisons and sustainability tips |

## One-time setup

1. Accept the GitHub invitation.
2. Install Git, VS Code, and Python 3.11+.
3. Set your Git identity:

```bash
git config --global user.name "Dishita Vaswani"
git config --global user.email "your-github-email@example.com"
```

4. Clone and open the project:

```bash
git clone https://github.com/dishitavaswani/SIH-Water-Footprints.git
cd SIH-Water-Footprints
code .
```

5. Switch to your branch:

```bash
git checkout feature/database
git pull origin feature/database
```

## Every time you start work

```bash
git checkout feature/database
git pull origin feature/database
git fetch origin
git merge origin/dev
```

Resolve conflicts in VS Code before continuing. If a conflict touches code owned by another teammate, ask them before deciding which version to retain.

## Build order

1. Identify credible water-footprint data sources and record source URL, publication, unit, and licence.
2. Save untouched source material as `raw_water_footprint.csv`.
3. Write `clean_dataset.py` to standardize names and values, preferably to litres per kilogram.
4. Generate and commit `cleaned_water_footprint.csv` only when its source permits distribution.
5. Define `WaterFootprint`, `ComparisonReference`, and `AltSuggestions` schemas.
6. Implement a repeatable seed script.
7. Implement `get_comparison()` and `get_tip()` in `lookup.py`.
8. Add an audit that compares Kuhu's model labels with available database entries.

## Data quality rules

- Never overwrite raw data; cleaning must create a separate output.
- State whether a value is per kg, per litre, per serving, or another unit.
- Do not silently convert units—document the formula.
- Avoid committing personal data or data with an unclear licence.
- Notify Aryaveer and Shaurya when lookup fields or response values change.

## Run your scripts

From the repository root, use commands like:

```bash
python database/scripts/clean_dataset.py
python database/scripts/seed_db.py
python database/scripts/audit_coverage.py
```

Before creating a pull request, verify that the cleaning script can run from a fresh clone and produces expected output.

## Save and push

```bash
git status
git add database/
git commit -m "feat: add cleaned water footprint dataset"
git push origin feature/database
```

## Copy-ready Antigravity prompts

Open the project folder in Antigravity, check that the active branch is `feature/database`, and use one prompt at a time. Review all source and licence information yourself before accepting a data change.

### Prompt 1 — inspect the data workspace

```text
You are working in SIH-Water-Footprints on branch feature/database. Inspect only database/ and the root README.md. Do not change files. Summarize the expected data flow from raw source to cleaned data to lookup result. List the schemas, scripts, data columns, and test cases that should be created. Do not inspect or modify other teammates' folders.
```

### Prompt 2 — define the dataset contract

```text
Work only in database/. Design a documented CSV schema for water-footprint records. Include item name, normalized item key, unit, total litres per kg, green water, blue water, grey water, source, and notes. Update database/README.md with the schema and explicit rules for source URLs, licences, and unit conversions. Do not invent water-footprint values and do not add downloaded data.
```

### Prompt 3 — implement deterministic cleaning

```text
Work only in database/scripts/clean_dataset.py and related database documentation. Implement a deterministic cleaning pipeline that reads raw_water_footprint.csv, standardizes item names and units, validates numeric values, and writes cleaned_water_footprint.csv. Invalid rows should be reported clearly rather than silently discarded. Explain the conversion assumptions in comments and documentation. Do not modify backend/.
```

### Prompt 4 — add schemas and lookups

```text
Work only in database/. Implement clear schema definitions for WaterFootprint, ComparisonReference, and AltSuggestions in models/schemas.py. Implement lookup helpers in lookup.py that return the data needed by the documented GET /footprint response, including comparison and sustainability tip. Keep the interface simple for Aryaveer's backend. Add example data only when clearly marked as sample/demo data.
```

### Prompt 5 — seed and coverage checks

```text
Work only in database/scripts/. Implement a seed script that can be rerun safely and an audit_coverage.py script that accepts a list of ML labels and reports which labels are missing from the cleaned dataset. Do not import Kuhu's model or change ml_model/. Document exact commands and expected output in database/README.md.
```

### Prompt 6 — review before commit

```text
Review uncommitted changes on feature/database. Confirm raw data is preserved, cleaned data is reproducible, units are documented, no licence or privacy problem is visible, and changes stay inside database/. Report findings and propose a single focused commit message. Do not commit or push.
```

Use focused commits: one for source documentation, one for schema changes, and one for a data-cleaning algorithm if possible.

## Create your pull request

1. Open the repository's **Pull requests** tab.
2. Create a PR with base `dev` and compare `feature/database`.
3. State dataset source(s), unit conversion, changed files, and test command(s).
4. Ask for review from Aryaveer when backend lookup behavior is affected.
5. Merge only after review and no conflicts.

After merge, sync your branch:

```bash
git checkout feature/database
git pull origin feature/database
git merge origin/dev
git push origin feature/database
```
