# Kuhu — ML Recognition Guide

## Your ownership

You own food image recognition on `feature/ml-recognition`.

Work only in `ml_model/` unless the team agrees on a cross-module interface change.

| File or folder | Your responsibility |
| --- | --- |
| `predict.py` | importable `predict_label(image_path)` function |
| `accuracy_test.py` | model evaluation harness |
| `models/` | model documentation, download location, and checksum |
| `sample_images/` | legal-to-commit test images |
| `README.md` | model setup, labels, limitations, and results |

## One-time setup

1. Accept the GitHub invitation.
2. Install Git, VS Code, and Python 3.11+.
3. Install your chosen model runtime, such as TensorFlow Lite or TensorFlow.
4. Configure Git:

```bash
git config --global user.name "Kuhu"
git config --global user.email "your-github-email@example.com"
```

5. Clone and enter your branch:

```bash
git clone https://github.com/dishitavaswani/SIH-Water-Footprints.git
cd SIH-Water-Footprints
code .
git checkout feature/ml-recognition
git pull origin feature/ml-recognition
```

## Every time you start work

```bash
git checkout feature/ml-recognition
git pull origin feature/ml-recognition
git fetch origin
git merge origin/dev
```

## Build order

1. Choose a food-classification model whose licence allows the intended use.
2. Document the source link, version, labels, input image size, licence, and file checksum in `ml_model/README.md`.
3. Define a simple, importable interface in `predict.py`:

```python
predict_label(image_path)  # returns label and confidence
```

4. Preprocess images exactly as the model requires.
5. Map model labels to database item names; share this mapping with Dishita.
6. Apply the required confidence rule: below `0.6`, return a manual-search fallback rather than a confident incorrect result.
7. Create `accuracy_test.py` to measure correct predictions on labelled images.
8. Document unsupported foods, poor-image cases, and model limitations.

## Model-file rules

- Do not commit large `.tflite`, `.h5`, `.onnx`, or similar model binaries; they are intentionally ignored.
- Provide a safe download source and SHA-256 checksum so all teammates use the same model.
- Commit only small test images that you have permission to distribute.
- Never upload private user images or credentials.

## Test before pushing

Run your evaluation harness from the repository root:

```bash
python ml_model/accuracy_test.py
```

Test at least:

- a clear, recognised food image;
- a low-quality or unrelated image;
- a confidence below `0.6`;
- a label that does not exist in the database.

Tell Aryaveer how the backend should call your function and what it returns. Tell Dishita every label that needs data coverage.

## Save and push

```bash
git status
git add ml_model/
git commit -m "feat: add confidence-aware food predictor"
git push origin feature/ml-recognition
```

## Copy-ready Antigravity prompts

Open the project in Antigravity, verify that the active branch is `feature/ml-recognition`, and use each prompt separately. Keep all source changes in `ml_model/`; never commit large model binaries or private images.

### Prompt 1 — inspect ML baseline

```text
You are working in SIH-Water-Footprints on branch feature/ml-recognition. Inspect only ml_model/, database/lookup interface documentation, and the root README.md. Do not edit files. Summarize the expected prediction interface, confidence behavior, expected label-to-database relationship, model-file constraints, and a safe implementation plan.
```

### Prompt 2 — define the model contract

```text
Work only in ml_model/README.md and ml_model/predict.py. Define a stable `predict_label(image_path)` interface that returns a label, confidence, and a machine-readable low-confidence/manual-search signal. Set the confidence threshold to 0.6. Document input requirements, errors, model source/version/licence/checksum fields, and label naming rules. Do not download or commit a model binary.
```

### Prompt 3 — implement prediction adapter

```text
Work only in ml_model/predict.py. Implement a clean adapter around a future TFLite food-classification model: validate the image path, load the runtime lazily, preprocess an image according to configurable model metadata, map output index to a label, and return the documented confidence-aware result. The code must fail with a clear setup message when the local model file is absent. Do not modify backend/ or database/.
```

### Prompt 4 — create evaluation harness

```text
Work only in ml_model/accuracy_test.py and ml_model/README.md. Implement an evaluation harness that reads labelled sample images, calls predict_label, reports total predictions, correct predictions, accuracy, low-confidence count, unknown-label count, and failures. It must continue evaluating after a single bad image and print a concise final summary. Document how to add legal sample images.
```

### Prompt 5 — database/backend handoff

```text
Do not edit database/ or backend/. Add a concise section to ml_model/README.md that tells Dishita and Aryaveer exactly what the prediction function returns, how low-confidence results must be handled, and how to maintain a label-to-database-item mapping. Include a few example result objects but no fabricated accuracy claims.
```

### Prompt 6 — review before commit

```text
Review uncommitted changes on feature/ml-recognition. Confirm changes stay in ml_model/, no model binary/private image/secret is staged, the confidence threshold is exactly 0.6, missing-model errors are understandable, and evaluation is reproducible. Report problems and propose a focused commit message. Do not commit or push.
```

## Create your pull request

1. Create a PR from `feature/ml-recognition` to `dev`.
2. Include the model source, licence, testing method, accuracy result, and confidence threshold behavior.
3. Ask Aryaveer to review the backend integration interface and Dishita to review label compatibility.
4. Merge only after review.

After merge:

```bash
git checkout feature/ml-recognition
git pull origin feature/ml-recognition
git merge origin/dev
git push origin feature/ml-recognition
```
