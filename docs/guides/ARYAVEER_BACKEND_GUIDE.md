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

## Copy-ready Antigravity prompts

Open the project folder in Antigravity, confirm that the active branch is `feature/backend-api`, and use these prompts **one at a time**. Review every change before accepting it.

### Prompt 1 — inspect the backend baseline

```text
You are working in the SIH-Water-Footprints repository on branch feature/backend-api. Inspect only the backend/ folder and the root README.md. Do not edit any files yet. Summarize the current FastAPI structure, missing dependencies, API contract, and the exact files that must change to add a basic health endpoint. Do not touch files outside backend/.
```

### Prompt 2 — create the app skeleton

```text
Work only in backend/. Implement a minimal FastAPI application in backend/app/main.py that can start with `uvicorn app.main:app --reload`. Add a GET /health endpoint returning JSON with a healthy status. Register API routes cleanly without changing the documented GET /footprint or POST /scan contract. Update backend/requirements.txt only if a dependency is necessary. Add concise code comments where decisions are not obvious. Then explain how to run and test the endpoint locally.
```

### Prompt 3 — add the footprint endpoint

```text
Work only in backend/. Implement GET /footprint with a required `item` query parameter. Keep the JSON response aligned with the root README API contract: item, total_litres_per_kg, green_water_litres, blue_water_litres, grey_water_litres, comparison, and tip. For now, isolate database access behind a helper so Dishita's database lookup can replace it later. Return a clear 404 response for an unknown item and 422 for invalid input. Do not edit database/ or mobile_app/. Add a small test or a manual verification instruction.
```

### Prompt 4 — prepare scan integration

```text
Work only in backend/. Implement POST /scan to accept an image upload safely. Define a clear adapter boundary for Kuhu's `predict_label(image_path)` function, but do not edit ml_model/. If confidence is below 0.6, return a response that asks the client to use manual search instead of claiming a food label. Validate file type and handle malformed uploads with useful errors. Document the expected response shape and how Shaurya can call the endpoint.
```

### Prompt 5 — configuration and CORS

```text
Work only in backend/. Add environment-based configuration and CORS settings in backend/app/core/config.py. Allow local Flutter development while keeping origins configurable by environment variable. Do not commit credentials, API keys, or a real production URL. Wire the configuration into the FastAPI app and update backend/README.md with setup variables and run commands.
```

### Prompt 6 — review before commit

```text
Review the current uncommitted changes on feature/backend-api. Check that changes are limited to backend/, no secrets or generated folders are included, the API contract has not accidentally changed, and the server can start. Report issues first. If the changes are safe, propose one concise Conventional Commit message but do not run git commit or git push.
```
