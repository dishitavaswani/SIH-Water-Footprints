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

## Copy-ready Antigravity prompts

Open the repository in Antigravity and verify the active branch is `feature/multilingual`. Use these prompts one at a time; do not accept machine-translated Hindi without review.

### Prompt 1 — inspect localization scope

```text
You are working in SIH-Water-Footprints on branch feature/multilingual. Inspect only multilingual/, mobile_app/ visible-string usage, and the root README.md. Do not edit files. List all user-facing strings currently needed for search, scanning, results, errors, and buttons. Propose a consistent ARB key naming convention and identify integration assumptions for Flutter.
```

### Prompt 2 — create ARB foundations

```text
Work only in multilingual/l10n/. Create or expand app_en.arb and app_hi.arb with matching keys for the initial user journey: search, scan, loading, not found, network error, low confidence, water-footprint headings, comparison, and tips. Preserve identical placeholder names in both files. Use clear English and carefully reviewed Hindi. Do not edit mobile_app/.
```

### Prompt 3 — enforce key parity

```text
Work only in multilingual/scripts/qa_check_arb.py. Implement a Python checker that reads app_en.arb and app_hi.arb, reports keys missing from either file, checks placeholder parity, exits non-zero on a mismatch, and prints a short success summary when both files match. Add a README example showing how to run it.
```

### Prompt 4 — manage verified Hindi overrides

```text
Work only in multilingual/data and multilingual/scripts. Define a safe JSON format for verified Hindi overrides and implement generate_hi_overrides.py to validate the format and generate/update output predictably. Keep human-reviewed text separate from unreviewed machine suggestions. Never include a translation-provider API key in committed files.
```

### Prompt 5 — prepare Flutter handoff

```text
Do not edit mobile_app/. Review the current ARB keys and produce a concise integration note for Shaurya: file paths, key names, placeholders, expected generated localization approach, and the command needed to run the parity check. Add this note to multilingual/README.md.
```

### Prompt 6 — review before commit

```text
Review uncommitted changes on feature/multilingual. Verify English/Hindi key and placeholder parity, valid JSON/ARB syntax, no API secrets, clear reviewed versus machine-generated text, and changes limited to multilingual/. Report issues and propose a focused commit message. Do not commit or push.
```

## Roadmap-specific Antigravity prompts (Phases 1–5)

### Phase 1 — Flutter i18n and translation experiment

```text
On branch feature/multilingual, implement Phase 1 only. Set up Flutter localization structure using flutter_localizations and intl. Create app_en.arb and app_hi.arb with matching initial keys: search, scan, waterFootprint, greenWater, blueWater, greyWater, and tryAnother. Write a standalone Python `translate(text: str, target_lang: str) -> str` experiment for Google Translate or Bhashini using environment variables only. Do not edit mobile_app/ integration code yet.
```

### Phase 2 — language toggle support and verified demo text

```text
On branch feature/multilingual, implement Phase 2 artifacts only. Define the expected Flutter language-toggle behavior for en/hi and document how API methods should append the `lang` parameter. Create a script that processes selected English comparison/tip strings through the translation adapter and writes a separate JSON override file for human verification. Add verified Hindi strings for demo-critical comparisons/tips. Do not claim machine translation is verified.
```

### Phase 3 — Hindi QA across the app

```text
On branch feature/multilingual, implement Phase 3 QA. Expand qa_check_arb.py so it reports keys missing in either ARB file and placeholder mismatches. Review the whole planned Search → Scan → Result flow in Hindi, identify awkward, missing, or truncated strings, and correct reviewed translations. Provide Shaurya with a concise list of changed keys and UI checks.
```

### Phase 4 — final readability pass

```text
On branch feature/multilingual, conduct the Phase 4 first-time-user readability pass. Review every Hindi string for respectful tone, clarity, consistent terminology for water footprint and manual retry, and sensible length for mobile screens. Record any remaining compromises or untranslated dynamic text in multilingual/README.md. Do not add API credentials.
```

### Phase 5 — accessibility-demo handoff

```text
Do not add new features. Create a short presentation handoff in multilingual/README.md showing how to demonstrate Hindi mode, which strings prove pan-India accessibility, and what fallback behavior is expected when a dynamic translation is not pre-verified.
```

## Git prompts for Vanshita

### Start and sync safely

```text
Run `git status --short --branch`; if anything is uncommitted, stop and report it. Otherwise run `git checkout feature/multilingual`, `git pull origin feature/multilingual`, `git fetch origin`, and `git merge origin/dev`. If an ARB or JSON conflict occurs, list the conflicting keys and do not silently drop a translation.
```

### Review, commit, and push a completed phase

```text
On feature/multilingual, run the ARB parity check and `git diff --check`. Confirm only multilingual/ files are staged, no translation API credentials exist, and English/Hindi placeholders match. Propose `multilingual: <specific completed work>`; after approval, commit and push only to feature/multilingual.
```

### Create a phase pull request

```text
Prepare a pull request from feature/multilingual into dev titled `multilingual: Phase <NUMBER> — <specific work>`. Include parity-check output, verified versus machine-generated translation notes, changed key list, Shaurya integration notes, and unresolved strings. Do not merge it yourself.
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
