# Aryaveer — Backend Guide

## Your ownership

You own the FastAPI backend on `feature/backend-api`.

Work only in `backend/` unless the team first agrees on a shared API-contract change.

| File or folder | Your responsibility |
| --- | --- |
| `backend/app/main.py` | FastAPI app setup and router registration |
| `backend/app/api/endpoints.py` | `GET /footprint` and `POST /scan` routes |
| `backend/app/core/config.py` | environment variables and CORS |
| `backend/app/services/translation_service.py` | translation fallback/caching |
| `backend/requirements.txt` | backend dependencies |
| `backend/Procfile` | deployment command |

## One-time setup

1. Accept Dishita's GitHub repository invitation.
2. Install Git, VS Code, and Python 3.11 or later.
3. Open a terminal and configure your Git identity:

```bash
git config --global user.name "Aryaveer"
git config --global user.email "your-github-email@example.com"
```

4. Clone the repository and open it in VS Code:

```bash
git clone https://github.com/dishitavaswani/SIH-Water-Footprints.git
cd SIH-Water-Footprints
code .
```

5. Move to your branch:

```bash
git checkout feature/backend-api
git pull origin feature/backend-api
```

6. Create and activate a Python environment, then install packages:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Every time you start work

From the project root:

```bash
git checkout feature/backend-api
git pull origin feature/backend-api
git fetch origin
git merge origin/dev
```

If Git reports a merge conflict, do not continue blindly. Open the conflicted files in VS Code, keep the intended code, remove conflict markers, then run:

```bash
git add <resolved-file>
git commit -m "chore: resolve merge conflict with dev"
```

## Build order

1. Add a health route and create the FastAPI app in `app/main.py`.
2. Add CORS settings so the mobile app can call the API.
3. Implement `GET /footprint?item=<product>`.
4. Call Dishita's database lookup layer rather than duplicating dataset logic.
5. Implement `POST /scan` to accept an image and use Kuhu's prediction interface.
6. Return the agreed response shape for both endpoints.
7. Add useful errors: missing item, unknown product, invalid image, and ML low confidence.
8. Add translation fallback only after the core English endpoint works.

## API contract you must preserve

`GET /footprint` returns an object like:

```json
{
  "item": "rice",
  "total_litres_per_kg": 2500,
  "green_water_litres": 1700,
  "blue_water_litres": 600,
  "grey_water_litres": 200,
  "comparison": "Equivalent to ...",
  "tip": "..."
}
```

Tell Shaurya before changing a field name, type, or endpoint path. Tell Vanshita if new user-facing strings need translation.

## Run and test locally

With the virtual environment active inside `backend/`:

```bash
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs>. Test at least:

- a valid product lookup;
- an unknown product;
- a missing query parameter;
- an image scan with a recognisable image;
- a scan whose confidence is below `0.6`.

Stop the server with `Ctrl+C`.

## Save and push your work

From the repository root:

```bash
git status
git add backend/
git commit -m "feat: add footprint lookup endpoint"
git push origin feature/backend-api
```

Use `git diff` before committing to make sure no `.env`, API keys, or unrelated files are included.

## Create your pull request

1. Visit <https://github.com/dishitavaswani/SIH-Water-Footprints>.
2. Select **Compare & pull request**.
3. Set the base branch to `dev` and compare branch to `feature/backend-api`.
4. Describe what you built and how you tested it.
5. Request review; merge only after approval.

After merging, update your branch before starting another task:

```bash
git checkout feature/backend-api
git pull origin feature/backend-api
git merge origin/dev
git push origin feature/backend-api
```
