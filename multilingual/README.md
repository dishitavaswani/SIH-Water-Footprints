# 🌐 Multilingual & Localization Pillar

**Module Owner:** Vanshita  
**Branch:** `feature/multilingual`  
**Supported Locales:** English (`en`), Hindi (`hi`)  
**Resource Directory:** `multilingual/l10n/` (Flutter ARB format) & `multilingual/data/` (JSON overrides)

---

## 📌 1. Overview & Architecture

The Multilingual Pillar provides end-to-end internationalization ($i18n$) across the SIH Water Footprints platform:
1. **Frontend App Localization (Flutter)**: Standard Application Resource Bundle (`.arb`) files in `multilingual/l10n/` (`app_en.arb` and `app_hi.arb`) consumed by Flutter's `AppLocalizations` for UI widgets, headers, status indicators, and error dialogues.
2. **Backend Dynamic Translation (FastAPI)**: Curated translation dictionary in `multilingual/data/verified_hi_overrides.json` and standalone translation helper in `multilingual/scripts/standalone_translate.py` for translating dynamic comparisons, food names, and sustainability tips when `lang=hi` is passed in queries.
3. **Automated QA & Integrity Validation**:
   - `multilingual/scripts/qa_check_arb.py`: Verifies 100% bidirectional key parity and placeholder integrity between English and Hindi ARB files.
   - `multilingual/scripts/generate_hi_overrides.py`: Validates, trims, and formats the Hindi overrides dictionary.

```
multilingual/
├── data/
│   └── verified_hi_overrides.json      # 82+ verified Hindi translation pairs
├── l10n/
│   ├── app_en.arb                      # English UI localization catalog (17 keys)
│   └── app_hi.arb                      # Hindi UI localization catalog (17 keys)
├── scripts/
│   ├── generate_hi_overrides.py        # Override normalization and validation script
│   ├── qa_check_arb.py                 # Automated ARB key & placeholder parity test
│   └── standalone_translate.py         # Standalone translate(text, lang) utility
└── README.md
```

---

## 📱 2. Flutter Mobile Integration Guide (Shaurya)

Shaurya's Flutter app uses standard Flutter localization (`flutter_localizations` + `intl`):

### A. Configuration in `pubspec.yaml`
```yaml
dependencies:
  flutter:
    sdk: flutter
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0

flutter:
  generate: true
```

### B. Accessing Localized Strings in Widgets
```dart
import 'package:flutter_gen/gen_l10n/app_localizations.dart';

// In any widget build method:
final l10n = AppLocalizations.of(context)!;

Text(l10n.appTitle);                    // "Water Footprint Tracker" or "जल पदचिह्न ट्रैकर"
Text(l10n.greenWater);                   // "Green Water (Rainwater)" or "हरा जल (वर्षा जल)"
Text(l10n.allValuesIn("litres/kg"));     // "All values in litres/kg" or "सभी मान लीटर/किग्रा में"
Text(l10n.loading);                      // "Calculating water footprint..." or "जल पदचिह्न की गणना की जा रही है..."
Text(l10n.itemNotFound);                 // "Item not found..." or "वस्तु नहीं मिली..."
```

---

## 🛠️ 3. Backend FastAPI Integration Guide (Aryaveer)

Aryaveer's FastAPI backend (`backend/app/api/endpoints.py` / `backend/app/services/translation_service.py`) handles bilingual query parameters:
- `GET /footprint/{item_name}?lang=hi`
- `POST /scan?lang=hi`

### Loading Overrides & Localizing Endpoint Responses
```python
import os
import json
from multilingual.scripts.standalone_translate import translate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OVERRIDES_PATH = os.path.join(BASE_DIR, "..", "multilingual", "data", "verified_hi_overrides.json")

def load_hindi_overrides() -> dict:
    """Loads verified Hindi translations dictionary."""
    if os.path.exists(OVERRIDES_PATH):
        with open(OVERRIDES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def localize_response(data: dict, lang: str = "en") -> dict:
    """
    Translates response fields when lang=hi, using exact overrides
    with fallback to standalone translation.
    """
    if not data or lang.lower() != "hi":
        return data

    overrides = load_hindi_overrides()

    item_name = data.get("item_name", "")
    comparison = data.get("comparison", "")
    tip = data.get("tip", "")

    return {
        **data,
        "item_name": overrides.get(item_name.lower(), translate(item_name, target_lang="hi")),
        "comparison": overrides.get(comparison.lower(), translate(comparison, target_lang="hi")),
        "tip": overrides.get(tip.lower(), translate(tip, target_lang="hi")),
        "unit": "लीटर/किग्रा"
    }
```

---

## 📋 4. ARB Key Inventory & Localization Catalog

| Key | English (`app_en.arb`) | Hindi (`app_hi.arb`) | Purpose / UI Placement |
| :--- | :--- | :--- | :--- |
| `appTitle` | Water Footprint Tracker | जल पदचिह्न ट्रैकर | App bar title |
| `search` | Search food items | खाद्य पदार्थ खोजें | Search bar label |
| `searchHint` | Type a food name (e.g., rice, apple)... | भोजन का नाम लिखें (जैसे चावल, सेब)... | Search bar placeholder |
| `scan` | Scan Food | भोजन स्कैन करें | Camera scan button |
| `waterFootprint` | Water Footprint | जल पदचिह्न | Result card header |
| `greenWater` | Green Water (Rainwater) | हरा जल (वर्षा जल) | Rainwater metric label |
| `blueWater` | Blue Water (Surface/Groundwater) | नीला जल (भूजल/सतही जल) | Irrigation metric label |
| `greyWater` | Grey Water (Pollution dilution) | धूसर जल (प्रदूषण जल) | Pollution metric label |
| `tryAnother` | Try Another Item | दूसरा आइटम आज़माएं | Reset search action |
| `litresPerKg` | litres/kg | लीटर/किग्रा | Standard metric unit |
| `comparisonTitle` | Real-world Equivalent | वास्तविक तुलना | Benchmark comparison card |
| `tipTitle` | Sustainability Tip | सतत सुझाव | Alternative suggestion card |
| `loading` | Calculating water footprint... | जल पदचिह्न की गणना की जा रही है... | Progress indicator status |
| `itemNotFound` | Item not found. Try searching another food. | वस्तु नहीं मिली। कृपया कोई अन्य खाद्य पदार्थ खोजें। | 404 error banner |
| `lowConfidence` | Could not clearly recognize the item. Please search manually. | वस्तु की पहचान स्पष्ट नहीं हो सकी। कृपया नाम लिखकर खोजें। | Scan low confidence fallback |
| `networkError` | Network error. Please check your connection. | नेटवर्क त्रुटि। कृपया अपना इंटरनेट कनेक्शन जांचें। | Connection failure banner |
| `allValuesIn` | All values in {unit} | सभी मान {unit} में | Dynamic unit label |

---

## 🚀 5. CLI Verification Commands

Run these automated verification commands from the repository root:

```bash
# 1. Automated ARB key parity and placeholder integrity test
python multilingual/scripts/qa_check_arb.py

# 2. Validate and normalize verified_hi_overrides.json
python multilingual/scripts/generate_hi_overrides.py

# 3. Test standalone translation engine
python multilingual/scripts/standalone_translate.py
```
