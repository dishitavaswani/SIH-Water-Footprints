# mobile_app — Flutter UI (Shaurya)

Flutter frontend for the Water Footprint App (SIH 2024).

## Branch

`feature/mobile-ui`

## Phase 1 Status ✅

| File                                      | Status                                         |
| ----------------------------------------- | ---------------------------------------------- |
| `lib/main.dart`                           | ✅ App entry + routing                         |
| `lib/models/footprint_result.dart`        | ✅ Data model                                  |
| `lib/services/footprint_api_service.dart` | ✅ GET /footprint + POST /scan + mock fallback |
| `lib/screens/search_screen.dart`          | ✅ Search UI + error + loading state           |
| `lib/screens/result_screen.dart`          | ✅ Green/Blue/Grey visual breakdown            |
| `lib/screens/scan_screen.dart`            | 🟡 Stub (Phase 2)                              |
| `lib/widgets/loading_spinner.dart`        | ✅                                             |
| `lib/widgets/footprint_visual_bar.dart`   | ✅ Coloured progress bars                      |
| `lib/widgets/error_widget.dart`           | ✅ Offline / 404 error card                    |

## Prerequisites

- Flutter SDK ≥ 3.0.0
- Android Studio or VS Code with Flutter extension
- An Android emulator or physical device

## Run

```bash
cd mobile_app
flutter pub get
flutter run
```

> **Phase 1 note:** `FootprintApiService` connects to `http://10.0.2.2:8000`
> (Android emulator localhost). If the backend isn't running yet, the service
> automatically returns mock data so you can develop the UI independently.

## API contract (agreed with Aryaveer)

### GET `/footprint?item=<name>&lang=<en|hi>`

```json
{
  "item": "rice",
  "green_wf": 1200,
  "blue_wf": 300,
  "grey_wf": 100,
  "unit": "litres/kg",
  "comparison": "Equivalent to ~10 full bathtubs.",
  "tip": "Try lentils — they use 50% less water than rice."
}
```

Returns `404` with `{"detail": "Item not found"}` if no match.

### POST `/scan?lang=<en|hi>`

Multipart upload, field name `file`. Returns same JSON shape as GET /footprint.

## Phase 2 (next integration)

- [ ] `ScanScreen`: add `image_picker`, send multipart to `POST /scan`
- [ ] `ResultScreen`: add `comparison` + `tip` from DB (Dishita)
- [ ] Language toggle → pass `lang` param via app-wide state (Vanshita)
