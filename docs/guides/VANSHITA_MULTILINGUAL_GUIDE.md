# Vanshita — Multilingual Guide

## Your ownership

You own localization on `feature/multilingual`.

Work only in `multilingual/` unless the team agrees that a new shared UI string or integration point is required.

| File or folder | Your responsibility |
| --- | --- |
| `l10n/app_en.arb` | canonical English keys and strings |
| `l10n/app_hi.arb` | matching Hindi strings |
| `data/verified_hi_overrides.json` | reviewed Hindi overrides |
| `scripts/standalone_translate.py` | translation-provider experiment/tool |
| `scripts/generate_hi_overrides.py` | override generation |
| `scripts/qa_check_arb.py` | ARB key-parity checks |

## One-time setup

1. Accept the GitHub invitation.
2. Install Git, VS Code, and Python 3.11+.
3. Install Flutter if you will test the strings in the mobile app.
4. Configure Git:

```bash
git config --global user.name "Vanshita"
git config --global user.email "your-github-email@example.com"
```

5. Clone, open, and select your branch:

```bash
git clone https://github.com/dishitavaswani/SIH-Water-Footprints.git
cd SIH-Water-Footprints
code .
git checkout feature/multilingual
git pull origin feature/multilingual
```

## Every time you start work

```bash
git checkout feature/multilingual
git pull origin feature/multilingual
git fetch origin
git merge origin/dev
```

## Build order

1. Establish a consistent key naming scheme, e.g. `searchTitle`, `scanButton`, `resultWaterFootprint`.
2. Add all initial English UI strings to `app_en.arb`.
3. Add the exact same keys to `app_hi.arb` with Hindi translations.
4. Store human-reviewed corrections in `verified_hi_overrides.json`.
5. Build a key-parity script that fails when English and Hindi keys differ.
6. Keep translation API experiments separate from final verified translations.
7. Work with Shaurya to connect generated localization files to the Flutter app.
8. Work with Aryaveer only if server response text needs localization.

## Translation quality rules

- Every English key must exist in Hindi; every Hindi key must exist in English.
- Keep placeholders identical in both languages, for example `{item}`.
- Do not put API tokens or provider keys in Git; use a local `.env` file.
- Human-review important user-facing Hindi text.
- Avoid translating product names when a locally familiar name is more helpful; document the choice.

## Test before pushing

From the project root:

```bash
python multilingual/scripts/qa_check_arb.py
```

If the mobile app integration is ready, also test language switching in Flutter. Check long Hindi text on smaller phone screens so buttons and result cards do not overflow.

## Save and push

```bash
git status
git add multilingual/
git commit -m "feat: add Hindi result screen translations"
git push origin feature/multilingual
```

## Create your pull request

1. Create a GitHub pull request from `feature/multilingual` into `dev`.
2. List changed keys, verified translations, and the parity-check result.
3. Ask Shaurya to review changes that affect Flutter UI text.
4. Merge only after review.

After merge:

```bash
git checkout feature/multilingual
git pull origin feature/multilingual
git merge origin/dev
git push origin feature/multilingual
```
