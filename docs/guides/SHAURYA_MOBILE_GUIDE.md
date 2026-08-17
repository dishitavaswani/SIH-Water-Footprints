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
