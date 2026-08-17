# SIH Water Footprint App — Team Collaboration Handbook

This guide is the shared workflow for Aryaveer, Dishita, Shaurya, Vanshita, and Kuhu. Follow it to work in parallel without overwriting anyone else's work.

## 1. Repository and branch model

Repository: <https://github.com/dishitavaswani/SIH-Water-Footprints>

| Branch | Purpose | Who uses it |
| --- | --- | --- |
| `main` | Stable, reviewed project version | Everyone reads; only the project lead merges into it |
| `dev` | Combined work that is ready for integration testing | Pull requests merge here |
| `feature/backend-api` | FastAPI API and backend services | Aryaveer |
| `feature/database` | Dataset, database, and lookups | Dishita |
| `feature/mobile-ui` | Flutter app and UI | Shaurya |
| `feature/multilingual` | English/Hindi localization | Vanshita |
| `feature/ml-recognition` | Food recognition and ML evaluation | Kuhu |

**Important:** Do not commit or push directly to `main`. Do not work on another teammate's feature branch without asking them first.

## 2. One-time setup for every teammate

### Create a GitHub account and accept access

1. Create a GitHub account at <https://github.com> if you do not have one.
2. Give your GitHub username to Dishita, who adds you as a repository collaborator.
3. Open the invitation email or GitHub notification and select **Accept invitation**.

### Install required tools

1. Install [Git for Windows](https://git-scm.com/download/win).
2. Install [Visual Studio Code](https://code.visualstudio.com/).
3. In VS Code, install the **GitHub Pull Requests and Issues** extension.
4. Install the technology for your task:
   - Aryaveer: Python 3.11+.
   - Dishita: Python 3.11+ and a database viewer if desired.
   - Shaurya: Flutter SDK, Android Studio, and an Android emulator or phone.
   - Vanshita: Python 3.11+; Flutter is useful for testing strings in the app.
   - Kuhu: Python 3.11+ and the ML libraries chosen by the team.

### Configure Git (run once)

Open VS Code, select **Terminal → New Terminal**, then run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-github-email@example.com"
```

Use the email address connected to your GitHub account.

### Clone the repository

In the folder where you keep projects, run:

```bash
git clone https://github.com/dishitavaswani/SIH-Water-Footprints.git
cd SIH-Water-Footprints
code .
```

If GitHub asks you to sign in while pushing, select **Sign in with your browser** and authorize GitHub.

## 3. Daily workflow for everyone

Run these commands at the beginning of every work session:

```bash
git checkout <your-feature-branch>
git pull origin <your-feature-branch>
git fetch origin
git merge origin/dev
```

Replace `<your-feature-branch>` with your assigned branch. Merging `origin/dev` brings already-integrated work into your branch. If Git reports a conflict, follow the conflict section below before you continue.

After completing one small, related piece of work:

```bash
git status
git add <file-or-folder-you-changed>
git commit -m "feat: short description of the change"
git push origin <your-feature-branch>
```

Examples:

```bash
git add backend/app/api/endpoints.py
git commit -m "feat: add footprint lookup endpoint"
git push origin feature/backend-api
```

Use clear commit prefixes:

| Prefix | Use for |
| --- | --- |
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation |
| `test:` | Tests |
| `refactor:` | Code cleanup without behavior change |
| `chore:` | Tooling, setup, or configuration |

## 4. Your individual branch and area

### Aryaveer — backend

```bash
git checkout feature/backend-api
git pull origin feature/backend-api
```

Work only under `backend/`:

- `app/main.py`: FastAPI application startup.
- `app/api/endpoints.py`: `GET /footprint` and `POST /scan` routes.
- `app/core/config.py`: environment configuration and CORS.
- `app/services/translation_service.py`: translation fallback and caching.
- `requirements.txt` and `Procfile`: dependencies and deployment configuration.

Before a pull request, run the backend locally:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to test the API.

### Dishita — database and data

```bash
git checkout feature/database
git pull origin feature/database
```

Work only under `database/`:

- `data/`: raw and cleaned water-footprint datasets.
- `models/schemas.py`: data/database schemas.
- `scripts/`: cleaning, seeding, and coverage scripts.
- `lookup.py`: comparisons and sustainability tips.

Keep original source data unchanged. Record data source URLs, licence, units, and cleaning decisions in `database/README.md`. Make output values consistent in litres per kilogram where possible.

### Shaurya — Flutter mobile app

```bash
git checkout feature/mobile-ui
git pull origin feature/mobile-ui
```

Work only under `mobile_app/`:

- `lib/screens/`: Search, Scan, and Result screens.
- `lib/models/`: API response models.
- `lib/services/`: HTTP calls to the backend.
- `lib/widgets/`: reusable UI, loading, and error states.

Before a pull request:

```bash
cd mobile_app
flutter pub get
flutter analyze
flutter test
flutter run
```

Use the shared API response shape from the root `README.md`. Do not hard-code a production API address; put it in a configurable constant.

### Vanshita — multilingual support

```bash
git checkout feature/multilingual
git pull origin feature/multilingual
```

Work only under `multilingual/`:

- `l10n/app_en.arb`: canonical English UI strings.
- `l10n/app_hi.arb`: matching Hindi strings.
- `data/verified_hi_overrides.json`: human-verified Hindi overrides.
- `scripts/`: translation and ARB parity tooling.

For every English key, add the same key to Hindi before pushing. Run the parity script when it is ready:

```bash
python multilingual/scripts/qa_check_arb.py
```

Never put passwords or API keys in scripts. Use a local `.env` file that is not committed.

### Kuhu — ML image recognition

```bash
git checkout feature/ml-recognition
git pull origin feature/ml-recognition
```

Work only under `ml_model/`:

- `predict.py`: the importable `predict_label(image_path)` function.
- `accuracy_test.py`: model accuracy evaluation.
- `sample_images/`: test images that can legally be committed.
- `models/`: documentation, download information, and checksums for the model.

Use a confidence threshold of `0.6`: lower-confidence results should fall back to a manual search prompt. Do not commit large model binaries; `.tflite` files are ignored. Document how teammates can obtain the exact model.

## 5. Creating a pull request

After pushing your work:

1. Go to <https://github.com/dishitavaswani/SIH-Water-Footprints>.
2. Select **Compare & pull request**, or open the **Pull requests** tab and select **New pull request**.
3. Set **base** to `dev` and **compare** to your feature branch.
4. Use a concise title, for example: `feat: add Hindi translation resources`.
5. In the description, state what changed, how you tested it, and any remaining work.
6. Request a teammate review when possible.
7. Merge only after review and checks pass. Use **Squash and merge** unless the team agrees otherwise.

Use this pull-request description template:

```md
## What changed
- 

## How I tested it
- 

## Notes / follow-up
- 
```

## 6. Integrating work: `dev` to `main`

The project lead performs integration after a pull request is approved:

```bash
git checkout dev
git pull origin dev
git merge --no-ff feature/<completed-feature>
git push origin dev
```

Prefer merging through the GitHub pull-request page because it records the review and makes conflicts clearer.

When `dev` is tested end-to-end, merge it into `main` through a pull request (`dev` → `main`). Before merging, verify:

- Backend endpoints run.
- App can call the intended backend API.
- Database data returns expected results.
- English and Hindi resources have matching keys.
- ML output handles low confidence safely.

After the demo-ready merge, create a tagged release:

```bash
git checkout main
git pull origin main
git tag -a v1.0-hackathon-submission -m "SIH hackathon submission"
git push origin main --tags
```

## 7. Handling merge conflicts

First, do not panic and do not delete files. Git marks conflicts in the affected file with `<<<<<<<`, `=======`, and `>>>>>>>`.

```bash
git status
```

1. Open each conflicted file in VS Code. Select **Accept Current Change**, **Accept Incoming Change**, or combine both intentionally.
2. Remove all conflict markers.
3. Test the changed code.
4. Finish the merge:

```bash
git add <resolved-files>
git commit -m "chore: resolve merge conflict with dev"
git push origin <your-feature-branch>
```

To cancel a merge that has not been committed:

```bash
git merge --abort
```

If unsure, stop and ask the file owner before resolving their code.

## 8. Useful recovery commands

### See what changed

```bash
git status
git diff
git log --oneline --graph --all
```

### Remove an accidental file from the next commit

```bash
git restore --staged <file>
```

### Discard a local, uncommitted change

```bash
git restore <file>
```

Only use the previous command if you are certain the work is not needed; it permanently removes your local uncommitted edits.

### Update your branch from `dev`

```bash
git checkout <your-feature-branch>
git fetch origin
git merge origin/dev
git push origin <your-feature-branch>
```

## 9. Team rules

1. Pull before coding; push at the end of each focused task.
2. Keep commits small and understandable.
3. Do not commit `.env`, passwords, API keys, personal data, or large ML model files.
4. Keep edits inside your owned module whenever possible.
5. Discuss changes to shared contracts—the API response, data schema, localization keys, or model label list—before changing them.
6. A pull request should explain what was changed and how it was tested.
7. If something blocks you for more than 20 minutes, message the team with the error and the branch name.
