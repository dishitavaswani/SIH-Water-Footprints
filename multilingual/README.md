# 🌐 Multilingual & Localization Pillar

**Module Owner:** Vanshita  
**Branch:** `feature/multilingual`  
**Supported Locales:** English (`en`), Hindi (`hi`)  
**Resource Directory:** `multilingual/l10n/` (Flutter ARB format) & `multilingual/data/` (JSON overrides)

---

## 📌 1. Overview & Architecture

The Multilingual Pillar provides end-to-end internationalization ($i18n$) for both the Flutter mobile application and FastAPI backend responses:
1. **Frontend App Localization (Flutter)**: Standard Application Resource Bundle (`.arb`) files in `multilingual/l10n/` (`app_en.arb` and `app_hi.arb`) for UI widgets, headers, and buttons.
2. **Backend Dynamic Translation (FastAPI)**: Curated translation dictionary in `multilingual/data/verified_hi_overrides.json` and standalone translation helper in `multilingual/scripts/standalone_translate.py` for translating dynamic comparisons, food names, and sustainability tips when `lang=hi`.
3. **Quality Assurance Tools**:
   - `multilingual/scripts/qa_check_arb.py`: Verifies 100% key parity between English and Hindi ARB files.
   - `multilingual/scripts/generate_hi_overrides.py`: Validates, trims, and normalizes the overrides dictionary.

```
multilingual/
├── data/
│   └── verified_hi_overrides.json      # Verified Hindi translation dictionary
├── l10n/
│   ├── app_en.arb                      # English UI localization catalog
│   └── app_hi.arb                      # Hindi UI localization catalog
├── scripts/
│   ├── generate_hi_overrides.py        # Override normalization and validation script
│   ├── qa_check_arb.py                 # ARB key parity verification test
│   └── standalone_translate.py         # Standalone translate(text, lang) utility
└── README.md
```

---

## 🛠️ 2. Backend FastAPI Integration Guide

Aryaveer's backend (`backend/app/api/endpoints.py` / `backend/app/services/translation_service.py`) handles bilingual requests for `/footprint/{item_name}?lang=hi` and `/scan?lang=hi`.

### Loading Overrides & Dynamic Translation

```python
import os
import json
from multilingual.scripts.standalone_translate import translate

# 1. Direct standalone translation helper
hindi_text = translate("Rice", target_lang="hi")  # Returns "चावल"
hindi_comp = translate("equivalent to ~10 bathtubs of water", target_lang="hi")  # Returns "लगभग 10 बाथटब पानी के बराबर"

# 2. Loading verified overrides in FastAPI endpoint handler
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OVERRIDES_PATH = os.path.join(BASE_DIR, "..", "multilingual", "data", "verified_hi_overrides.json")

def get_translation_map() -> dict:
    if os.path.exists(OVERRIDES_PATH):
        with open(OVERRIDES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def localize_response(response_dict: dict, lang: str = "en") -> dict:
    if lang.lower() != "hi":
        return response_dict

    overrides = get_translation_map()

    item_name = response_dict.get("item_name", "")
    comparison = response_dict.get("comparison", "")
    tip = response_dict.get("tip", "")

    # Localize item name, comparison, and sustainability tip
    return {
        **response_dict,
        "item_name": overrides.get(item_name.lower(), translate(item_name, target_lang="hi")),
        "comparison": overrides.get(comparison.lower(), translate(comparison, target_lang="hi")),
        "tip": overrides.get(tip.lower(), translate(tip, target_lang="hi")),
        "unit": "लीटर/किग्रा"
    }
```

---

## 📱 3. Flutter ARB Localization Catalog

Every user-facing string added to `multilingual/l10n/app_en.arb` must have an identical key in `multilingual/l10n/app_hi.arb`.

### Current ARB Key Table

| ARB Key | English (`app_en.arb`) | Hindi (`app_hi.arb`) |
| :--- | :--- | :--- |
| `appTitle` | Water Footprint Tracker | जल पदचिह्न ट्रैकर |
| `search` | Search food items | खाद्य पदार्थ खोजें |
| `searchHint` | Type a food name (e.g., rice, apple)... | भोजन का नाम लिखें (जैसे चावल, सेब)... |
| `scan` | Scan Food | भोजन स्कैन करें |
| `waterFootprint` | Water Footprint | जल पदचिह्न |
| `greenWater` | Green Water (Rainwater) | हरा जल (वर्षा जल) |
| `blueWater` | Blue Water (Surface/Groundwater) | नीला जल (भूजल/सतही जल) |
| `greyWater` | Grey Water (Pollution dilution) | धूसर जल (प्रदूषण जल) |
| `tryAnother` | Try Another Item | दूसरा आइटम आज़माएं |
| `litresPerKg` | litres/kg | लीटर/किग्रा |
| `comparisonTitle` | Real-world Equivalent | वास्तविक तुलना |
| `tipTitle` | Sustainability Tip | सतत सुझाव |

---

## 🚀 4. CLI Validation Commands

Run these commands from the repository root:

```bash
# 1. Run ARB key parity check
python multilingual/scripts/qa_check_arb.py

# 2. Validate and format verified_hi_overrides.json
python multilingual/scripts/generate_hi_overrides.py

# 3. Test standalone translation engine
python multilingual/scripts/standalone_translate.py
```
