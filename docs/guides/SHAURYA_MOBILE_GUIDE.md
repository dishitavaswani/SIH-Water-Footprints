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
