# Shaurya — Flutter Mobile App Guide

## Your ownership

You own the Flutter app on `feature/mobile-ui`.

Work only in `mobile_app/` unless an agreed shared API or localization contract requires another change.

| File or folder | Your responsibility |
| --- | --- |
| `lib/main.dart` | app setup and navigation |
| `lib/models/` | footprint data model |
| `lib/screens/` | search, scan, and result screens |
| `lib/services/` | backend HTTP client |
| `lib/widgets/` | reusable visual, loading, and error widgets |
| `pubspec.yaml` | Flutter dependencies |

## One-time setup

1. Accept the GitHub invitation.
2. Install Git, VS Code, Flutter SDK, Android Studio, and an emulator or test phone.
3. In VS Code install the Flutter and Dart extensions.
4. Configure Git:

```bash
git config --global user.name "Shaurya"
git config --global user.email "your-github-email@example.com"
```

5. Clone and open the repository:

```bash
git clone https://github.com/dishitavaswani/SIH-Water-Footprints.git
cd SIH-Water-Footprints
code .
```

6. Open your branch and install Flutter packages:

```bash
git checkout feature/mobile-ui
git pull origin feature/mobile-ui
cd mobile_app
flutter pub get
```

## Every time you start work

From the project root:

```bash
git checkout feature/mobile-ui
git pull origin feature/mobile-ui
git fetch origin
git merge origin/dev
```

Then from `mobile_app/`:

```bash
flutter pub get
```

## Build order

1. Create application theme, routing, and a simple start screen.
2. Create `FootprintResult` matching Aryaveer's API response exactly.
3. Create a configurable API base URL; do not hard-code a personal computer IP as production configuration.
4. Build `SearchScreen` with loading, empty, successful, and error states.
5. Build `ResultScreen` with total footprint, green/blue/grey bars, comparison, and tip.
6. Build `ScanScreen` with camera/photo selection.
7. Connect scan/upload calls to `POST /scan`.
8. Handle no-network, 404, bad response, and low-confidence ML responses gracefully.
9. Coordinate all visible strings with Vanshita before finalizing labels.

## API rules

Call `GET /footprint?item=<product>` for text search. `POST /scan` accepts an image and returns a recognised item plus footprint data.

Before changing any API field, endpoint, or error behavior, discuss it with Aryaveer and Dishita. Test against the backend's `/docs` page before merging.

## Test before pushing

From `mobile_app/`:

```bash
flutter analyze
flutter test
flutter run
```

Manually test:

- a valid product search;
- an unknown product;
- a loading state;
- offline/API failure;
- an image scan;
- a low-confidence result;
- the result layout on a small phone screen.

## Save and push

From the repository root:

```bash
git status
git add mobile_app/
git commit -m "feat: add footprint results screen"
git push origin feature/mobile-ui
```

## Copy-ready Antigravity prompts

Open the repository in Antigravity, confirm the branch is `feature/mobile-ui`, and run the prompts one at a time. Keep all changes inside `mobile_app/` unless the team approves a shared contract edit.

### Prompt 1 — inspect the Flutter baseline

```text
You are working in SIH-Water-Footprints on branch feature/mobile-ui. Inspect only mobile_app/ and the root README.md. Do not edit files. Report the current Flutter project state, missing setup, required screens, API response fields, and a small implementation plan for Search, Scan, and Result screens.
```

### Prompt 2 — bootstrap the app

```text
Work only in mobile_app/. Create a minimal runnable Flutter app with Material theme, named routes or clear navigation, and a temporary home screen that links to search and scan flows. Update pubspec.yaml only for necessary packages. Do not add generated platform folders unless Flutter itself creates them. Give exact flutter commands to run, analyze, and test the app.
```

### Prompt 3 — add the API model and client

```text
Work only in mobile_app/lib/models and mobile_app/lib/services. Implement a FootprintResult model matching the documented backend JSON response exactly. Implement a configurable FootprintApiService for GET /footprint?item=<product> and a placeholder-safe POST /scan image upload method. Handle timeout, invalid JSON, 404, and server errors. Do not hard-code a personal IP address or change backend files.
```

### Prompt 4 — build search and result UI

```text
Work only in mobile_app/lib/screens and mobile_app/lib/widgets. Build a SearchScreen with text input, search action, loading state, empty state, API error state, and navigation to ResultScreen. Build ResultScreen to show item name, total litres per kg, green/blue/grey water breakdown, comparison, and tip. Keep visible strings easy to move to localization later. Ensure the layout works on a small phone screen.
```

### Prompt 5 — build the scan flow

```text
Work only in mobile_app/. Add a ScanScreen that lets the user choose or capture an image, shows upload progress, calls the scan service, and displays a low-confidence/manual-search fallback when confidence is below 0.6. Handle camera permission denial and no-network errors gracefully. Do not edit Kuhu's model files or Aryaveer's backend.
```

### Prompt 6 — quality review

```text
Review current changes on feature/mobile-ui. Run or specify `flutter analyze` and `flutter test`. Check for API-model mismatches, hard-coded secrets or URLs, overflow risks, missing loading/error states, and edits outside mobile_app/. Report issues and propose a focused commit message. Do not commit or push.
```

## Roadmap-specific Antigravity prompts (Phases 1–5)

### Phase 1 — Flutter search foundation

```text
On branch feature/mobile-ui, implement Phase 1 only. Build a Flutter scaffold with Navigator, SearchScreen, ResultScreen, and FootprintResult. SearchScreen needs a TextField and Search button. ResultScreen displays item name plus green_wf, blue_wf, grey_wf, unit, comparison, and tip passed as data. Implement FootprintApiService.getFootprint(String item) with the http package and initially support a clearly isolated mock response until Aryaveer's backend is ready. Do not edit backend/.
```

### Phase 2 — camera, scan, and visual breakdown

```text
On branch feature/mobile-ui, implement Phase 2 only. Add ScanScreen using image_picker to capture/select an image. Upload it as multipart/form-data to POST <base_url>/scan, parse the response into FootprintResult, then navigate to ResultScreen. Display green/blue/grey values as three accessible colored horizontal bars and show comparison/tip below. Handle camera permissions, image selection cancellation, upload failure, and low-confidence manual-search fallback.
```

### Phase 3 — full localization integration

```text
On branch feature/mobile-ui, implement Phase 3 only. Replace hard-coded user-facing strings in SearchScreen, ScanScreen, ResultScreen, loading states, and errors with AppLocalizations keys from Vanshita's ARB resources. Wire the shared language toggle into the application state and ensure API calls pass `lang=en` or `lang=hi`. List any required missing ARB keys; do not edit multilingual/ directly.
```

### Phase 4 — polish and resilience

```text
On branch feature/mobile-ui, implement Phase 4 only. Add friendly loading spinners and error widgets for no internet, timeout, item-not-found (404), invalid scan, and low confidence. Use a simple loading/success/error state model. Improve spacing, readability, and app icon setup without adding secrets or generated build files. Test the UI on a small screen.
```

### Phase 5 — demo preparation

```text
Do not add unrelated features. Prepare a repeatable live-demo checklist in mobile_app/README.md: text search → result → scan → result → language toggle. Include fallback behavior if the API or image recognition is unavailable. Confirm the order Shaurya should follow during the team presentation.
```

## Git prompts for Shaurya

### Start and sync safely

```text
In SIH-Water-Footprints, run `git status --short --branch`. If uncommitted changes exist, stop and report them. Otherwise run `git checkout feature/mobile-ui`, `git pull origin feature/mobile-ui`, `git fetch origin`, and `git merge origin/dev`. If Flutter files conflict, list each file and explain whether the conflict affects an API contract, localization, or UI before changing it.
```

### Review, commit, and push a completed phase

```text
On feature/mobile-ui, run `flutter analyze`, `flutter test`, `git diff --check`, and inspect the staged files. Confirm only mobile_app/ files are staged and no build output, signing key, personal base URL, or secret is included. Propose `mobile: <specific completed work>`; after approval, commit and push only to feature/mobile-ui.
```

### Create a phase pull request

```text
Prepare a pull request from feature/mobile-ui into dev titled `mobile: Phase <NUMBER> — <specific work>`. Include screenshots/recording if UI changed, exact Flutter test results, tested backend URL configuration, API dependency notes, localization dependency notes, and known limitations. Do not merge it yourself.
```

Do not commit `build/`, local Android signing keys, or environment secrets.

## Create your pull request

1. On GitHub choose **New pull request**.
2. Set base to `dev`; set compare to `feature/mobile-ui`.
3. Add screenshots or a short screen recording when UI changes are visible.
4. List commands you ran: `flutter analyze`, `flutter test`, and device testing.
5. Request review; merge after approval.

After merge:

```bash
git checkout feature/mobile-ui
git pull origin feature/mobile-ui
git merge origin/dev
git push origin feature/mobile-ui
```
