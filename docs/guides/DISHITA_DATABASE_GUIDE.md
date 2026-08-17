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
