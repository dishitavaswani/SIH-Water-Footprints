import os
import sys
import json
import urllib.request
import urllib.parse
from typing import Optional

# Ensure UTF-8 output on Windows console
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
OVERRIDES_PATH = os.path.join(BASE_DIR, "data", "verified_hi_overrides.json")

# In-memory dictionary fallback
LOCAL_DICTIONARY = {
    "water footprint tracker": "जल पदचिह्न ट्रैकर",
    "search food items": "खाद्य पदार्थ खोजें",
    "type a food name (e.g., rice, apple)...": "भोजन का नाम लिखें (जैसे चावल, सेब)...",
    "scan food": "भोजन स्कैन करें",
    "water footprint": "जल पदचिह्न",
    "green water (rainwater)": "हरा जल (वर्षा जल)",
    "blue water (surface/groundwater)": "नीला जल (भूजल/सतही जल)",
    "grey water (pollution dilution)": "धूसर जल (प्रदूषण जल)",
    "try another item": "दूसरा आइटम आज़माएं",
    "litres/kg": "लीटर/किग्रा",
    "real-world equivalent": "वास्तविक तुलना",
    "sustainability tip": "सतत सुझाव",
    "rice": "चावल",
    "wheat": "गेहूं",
    "apple": "सेब",
    "banana": "केला",
    "beef": "गोमांस",
    "chicken": "चिकन",
    "milk": "दूध",
    "potato": "आलू",
    "tomato": "टमाटर",
    "coffee": "कॉफ़ी",
    "chocolate": "चॉकलेट",
    "almond": "बादाम",
    "almonds": "बादाम",
    "pork": "सूअर का मांस",
    "eggs": "अंडे",
    "cheese": "पनीर",
    "butter": "मक्खन",
    "bread": "रोटी",
    "orange": "संतरा",
    "tea": "चाय",
    "sugar": "चीनी",
    "sugarcane": "गन्ना",
    "pulses": "दालें",
    "soybeans": "सोयाबीन",
    "corn": "मक्का",
    "maize": "मक्का",
    "cherry": "चेरी",
    "chilli": "मिर्च",
    "coconut": "नारियल",
    "cucumber": "खीरा",
    "jowar": "ज्वार",
    "lemon": "नींबू",
    "makhana": "मखाना",
    "papaya": "पपीता",
    "pearl_millet": "बाजरा",
    "pineapple": "अनानास",
    "pizza": "पिज़्ज़ा",
    "hamburger": "हैमबर्गर",
    "french_fries": "फ्रेंच फ्राइज़",
    "apple_pie": "एप्पल पाई",
    "chicken_curry": "चिकन करी"
}

def load_verified_overrides() -> dict:
    """Loads verified Hindi overrides from JSON file."""
    if os.path.exists(OVERRIDES_PATH):
        try:
            with open(OVERRIDES_PATH, mode='r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def _call_cloud_translate_api(text: str, target_lang: str, api_key: str) -> Optional[str]:
    """
    Calls Google Cloud Translation API v2 if API key is provided.
    Endpoint: https://translation.googleapis.com/language/translate/v2
    """
    try:
        url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
        payload = json.dumps({
            "q": text,
            "target": target_lang,
            "format": "text"
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            translations = data.get("data", {}).get("translations", [])
            if translations:
                return translations[0].get("translatedText")
    except Exception as e:
        # Silently fall back to offline dictionary on connection/auth errors
        pass
    return None

def _translate_offline(text: str, target_lang: str) -> str:
    """
    Offline fallback dictionary & phrase translator for Hindi.
    """
    if not text:
        return ""

    if target_lang != "hi":
        return text

    clean_text = text.strip()
    lower_text = clean_text.lower()

    # 1. Check verified overrides file
    overrides = load_verified_overrides()
    if clean_text in overrides:
        return overrides[clean_text]
    if lower_text in overrides:
        return overrides[lower_text]

    # 2. Check local built-in dictionary
    if lower_text in LOCAL_DICTIONARY:
        return LOCAL_DICTIONARY[lower_text]

    # 3. Dynamic template replacements for comparisons and tips
    translated_text = clean_text

    # Comparison template: "equivalent to ~10 bathtubs of water"
    if "equivalent to ~" in translated_text.lower():
        translated_text = (
            translated_text
            .replace("equivalent to ~", "लगभग ")
            .replace("of water", "पानी के बराबर")
            .replace("bathtubs", "बाथटब")
            .replace("bathtub", "बाथटब")
            .replace("buckets", "बाल्टी")
            .replace("bucket", "बाल्टी")
            .replace("standard water bottles", "पानी की बोतलें")
            .replace("standard water bottle", "पानी की बोतल")
            .replace("showers", "शॉवर")
            .replace("shower", "शॉवर")
            .replace("swimming pools", "स्विमिंग पूल")
            .replace("swimming pool", "स्विमिंग पूल")
            .replace("glasses of water", "गिलास पानी")
            .replace("glass of water", "गिलास पानी")
        )
        return translated_text

    # Sustainability tip template: "Consider replacing with..."
    if "consider replacing with" in translated_text.lower():
        translated_text = (
            translated_text
            .replace("Consider replacing with", "कम पानी की खपत के लिए")
            .replace("for lower water consumption", "से बदलने पर विचार करें")
        )
        return translated_text

    if "conserve water by choosing locally grown, seasonal produce" in translated_text.lower():
        return "स्थानीय रूप से उगाए गए, मौसमी उत्पाद चुनकर जल संरक्षण करें।"

    # Word-by-word replacement fallback for simple phrases
    words = clean_text.split()
    translated_words = [LOCAL_DICTIONARY.get(w.lower(), w) for w in words]
    return " ".join(translated_words)

def translate(text: str, target_lang: str = "hi") -> str:
    """
    Translates text to target language.
    Uses Google Cloud Translate if TRANSLATE_API_KEY / GOOGLE_TRANSLATE_API_KEY
    environment variable is configured; otherwise falls back cleanly to local dictionary.
    """
    if not text:
        return ""

    if target_lang == "en":
        return text

    api_key = os.getenv("TRANSLATE_API_KEY") or os.getenv("GOOGLE_TRANSLATE_API_KEY")

    if api_key:
        cloud_result = _call_cloud_translate_api(text, target_lang, api_key)
        if cloud_result:
            return cloud_result

    return _translate_offline(text, target_lang)

if __name__ == '__main__':
    print("=" * 65)
    print(" TESTING STANDALONE TRANSLATION (English -> Hindi)")
    print("=" * 65)

    test_phrases = [
        "Water Footprint Tracker",
        "Search food items",
        "Scan Food",
        "Green Water (Rainwater)",
        "Blue Water (Surface/Groundwater)",
        "Grey Water (Pollution dilution)",
        "rice",
        "beef",
        "apple",
        "coffee",
        "equivalent to ~10 bathtubs of water",
        "Conserve water by choosing locally grown, seasonal produce."
    ]

    for phrase in test_phrases:
        result = translate(phrase, target_lang="hi")
        print(f"EN: {phrase:<50}\nHI: {result}\n")
