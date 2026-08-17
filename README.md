# SIH Water Footprint App

A five-person Smart India Hackathon project that helps users understand the water footprint of agricultural products through search, camera recognition, and multilingual results.

## Team ownership

| Member | Branch | Area |
| --- | --- | --- |
| Aryaveer | `feature/backend-api` | FastAPI backend and API endpoints |
| Dishita | `feature/database` | Data curation, database schema, and lookup logic |
| Shaurya | `feature/mobile-ui` | Flutter application and UI |
| Vanshita | `feature/multilingual` | English/Hindi translations and translation QA |
| Kuhu | `feature/ml-recognition` | Food image recognition and model evaluation |

## Collaboration workflow

`main` contains reviewed, stable code. Each feature branch opens a pull request to `dev`; tested work in `dev` is then merged into `main`.

```bash
git checkout feature/<your-area>
git pull origin feature/<your-area>
# make a focused change
git add <files>
git commit -m "feat: describe your change"
git push origin feature/<your-area>
```

Open a pull request from your feature branch to `dev`. Do not push directly to `main` or delete another member’s branch.

## Initial API contract

### `GET /footprint`

Accepts an `item` product-name query parameter and returns the product, total litres per kilogram, green/blue/grey water values, comparison, and sustainability tip.

### `POST /scan`

Accepts an image upload and returns a recognised product label and confidence, followed by the same footprint data as `GET /footprint`.

## Layout

- `backend/` — FastAPI server
- `database/` — datasets, schemas, seeding, and lookups
- `mobile_app/` — Flutter app
- `multilingual/` — localization resources and tooling
- `ml_model/` — image-recognition model and evaluation
