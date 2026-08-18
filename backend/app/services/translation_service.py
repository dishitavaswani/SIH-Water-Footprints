"""Scalable Translation Service with layered provider architecture, verified agricultural glossary,
persistent structured caching, and pluggable external translation providers.

Resolution Priority:
1. Verified glossary term (domain-specific scientific & agricultural terminology)
2. Verified sentence translation (curated overrides/sentences)
3. Cached translation (L1 In-Memory + L2 Persistent SQLite cache)
4. Translation-engine fallback (Pluggable Cloud / Indian Regional / Template Engine)
5. English fallback (canonical source)
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Ensure repository root is on sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from multilingual.registry import normalize_language_code, is_supported_language
from multilingual.glossary import get_glossary_translation


def format_cache_key(source_lang: str, text: str, target_lang: str) -> str:
    """Constructs a standard structured cache key: 'source_lang|source_text|target_lang'.
    
    Example: 'en|Rice requires approximately 1600 litres/kg|mr'
    """
    s_lang = (source_lang or "en").strip().lower()
    t_lang = (target_lang or "").strip().lower()
    clean_text = (text or "").strip()
    return f"{s_lang}|{clean_text}|{t_lang}"


# ─────────────────────────────────────────────────────────────────────────────
# 1. Base Provider Abstractions
# ─────────────────────────────────────────────────────────────────────────────

class BaseTranslationProvider(ABC):
    """Abstract interface for any translation source."""

    @abstractmethod
    def get_translation(self, text: str, target_lang: str) -> Optional[str]:
        """Returns the translated text or None if the provider cannot handle it."""
        pass


class BaseCacheProvider(ABC):
    """Abstract interface for translation caching with structured key representation."""

    @abstractmethod
    def get(self, text: str, target_lang: str, source_lang: str = "en") -> Optional[str]:
        pass

    @abstractmethod
    def set(self, text: str, target_lang: str, translation: str, source_lang: str = "en") -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass


# ─────────────────────────────────────────────────────────────────────────────
# 2. In-Memory Cache Provider (L1 Fast Cache)
# ─────────────────────────────────────────────────────────────────────────────

class InMemoryCacheProvider(BaseCacheProvider):
    """Fast in-memory cache keyed by structured 'source_lang|source_text|target_lang'."""

    def __init__(self) -> None:
        self._cache: Dict[str, str] = {}

    def get(self, text: str, target_lang: str, source_lang: str = "en") -> Optional[str]:
        if not text or not target_lang:
            return None
        key = format_cache_key(source_lang, text, target_lang)
        return self._cache.get(key)

    def set(self, text: str, target_lang: str, translation: str, source_lang: str = "en") -> None:
        if not text or not target_lang or not translation:
            return
        # Do not cache obvious error strings or empty values
        clean_trans = translation.strip()
        if not clean_trans or clean_trans.lower().startswith(("error:", "exception:", "404", "failed:")):
            return
        key = format_cache_key(source_lang, text, target_lang)
        self._cache[key] = clean_trans

    def clear(self) -> None:
        self._cache.clear()

    def size(self) -> int:
        return len(self._cache)

    def contains(self, text: str, target_lang: str, source_lang: str = "en") -> bool:
        key = format_cache_key(source_lang, text, target_lang)
        return key in self._cache


# ─────────────────────────────────────────────────────────────────────────────
# 3. SQLite Cache Provider (L2 Persistent Cache)
# ─────────────────────────────────────────────────────────────────────────────

class SQLiteCacheProvider(BaseCacheProvider):
    """Resilient SQLite persistent translation cache.
    
    Stores entries persistently across server sessions and restarts, enabling
    seamless offline lookups without external network or infrastructure dependencies.
    """

    def __init__(self, db_path: Optional[Path] = None) -> None:
        self.db_path = db_path or (REPO_ROOT / "multilingual" / "data" / "translation_cache.db")
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path), timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def _init_db(self) -> None:
        conn = None
        try:
            conn = self._get_connection()
            conn.execute("""
                CREATE TABLE IF NOT EXISTS translation_cache (
                    cache_key TEXT PRIMARY KEY,
                    source_lang TEXT NOT NULL,
                    source_text TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
        except Exception:
            # Graceful degradation: never crash on DB initialization errors
            pass
        finally:
            if conn:
                conn.close()

    def get(self, text: str, target_lang: str, source_lang: str = "en") -> Optional[str]:
        if not text or not target_lang:
            return None
        key = format_cache_key(source_lang, text, target_lang)
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT translated_text FROM translation_cache WHERE cache_key = ?;",
                (key,)
            )
            row = cursor.fetchone()
            if row and row[0]:
                return str(row[0])
        except Exception:
            pass
        finally:
            if conn:
                conn.close()
        return None

    def set(self, text: str, target_lang: str, translation: str, source_lang: str = "en") -> None:
        if not text or not target_lang or not translation:
            return
        clean_trans = translation.strip()
        if not clean_trans or clean_trans.lower().startswith(("error:", "exception:", "404", "failed:")):
            return

        key = format_cache_key(source_lang, text, target_lang)
        clean_source_text = text.strip()
        clean_s_lang = (source_lang or "en").strip().lower()
        clean_t_lang = target_lang.strip().lower()

        conn = None
        try:
            conn = self._get_connection()
            conn.execute("""
                INSERT INTO translation_cache (cache_key, source_lang, source_text, target_lang, translated_text)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    translated_text = excluded.translated_text,
                    created_at = CURRENT_TIMESTAMP;
            """, (key, clean_s_lang, clean_source_text, clean_t_lang, clean_trans))
            conn.commit()
        except Exception:
            pass
        finally:
            if conn:
                conn.close()

    def clear(self) -> None:
        conn = None
        try:
            conn = self._get_connection()
            conn.execute("DELETE FROM translation_cache;")
            conn.commit()
        except Exception:
            pass
        finally:
            if conn:
                conn.close()

    def count(self) -> int:
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM translation_cache;")
            row = cursor.fetchone()
            return int(row[0]) if row else 0
        except Exception:
            return 0
        finally:
            if conn:
                conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# 4. Hybrid L1 (Memory) + L2 (SQLite) Cache Provider
# ─────────────────────────────────────────────────────────────────────────────

class HybridCacheProvider(BaseCacheProvider):
    """Two-tier caching strategy:
    - Tier 1: In-memory hash map for microsecond lookups
    - Tier 2: Persistent SQLite store for cold starts and offline durability
    """

    def __init__(self, mem_cache: Optional[InMemoryCacheProvider] = None, sql_cache: Optional[SQLiteCacheProvider] = None) -> None:
        self.mem = mem_cache or InMemoryCacheProvider()
        self.sql = sql_cache or SQLiteCacheProvider()

    def get(self, text: str, target_lang: str, source_lang: str = "en") -> Optional[str]:
        # Check L1 memory cache
        try:
            val = self.mem.get(text, target_lang, source_lang=source_lang)
            if val is not None:
                return val
        except Exception:
            pass

        # Check L2 SQLite cache
        try:
            val = self.sql.get(text, target_lang, source_lang=source_lang)
            if val is not None:
                # Backfill L1 memory cache
                try:
                    self.mem.set(text, target_lang, val, source_lang=source_lang)
                except Exception:
                    pass
                return val
        except Exception:
            pass

        return None

    def set(self, text: str, target_lang: str, translation: str, source_lang: str = "en") -> None:
        try:
            self.mem.set(text, target_lang, translation, source_lang=source_lang)
        except Exception:
            pass
        try:
            self.sql.set(text, target_lang, translation, source_lang=source_lang)
        except Exception:
            pass

    def clear(self) -> None:
        try:
            self.mem.clear()
        except Exception:
            pass
        try:
            self.sql.clear()
        except Exception:
            pass


# ─────────────────────────────────────────────────────────────────────────────
# 5. Verified Glossary Provider (Tier 1 Priority)
# ─────────────────────────────────────────────────────────────────────────────

class GlossaryTranslationProvider(BaseTranslationProvider):
    """Resolves verified scientific & agricultural terminology with highest priority.
    
    Prevents machine translation from corrupting standard scientific concepts
    such as 'Green Water' or 'Evapotranspiration'.
    """

    def get_translation(self, text: str, target_lang: str) -> Optional[str]:
        if not text or not target_lang:
            return None
        return get_glossary_translation(text.strip(), target_lang.strip().lower())


# ─────────────────────────────────────────────────────────────────────────────
# 6. Verified Translation Provider (Tier 2 Priority)
# ─────────────────────────────────────────────────────────────────────────────

class VerifiedTranslationProvider(BaseTranslationProvider):
    """Loads and resolves verified sentence overrides and item dictionaries.
    
    Supports:
    - multilingual/data/verified_hi_overrides.json
    - multilingual/data/overrides/<lang>.json
    - multilingual/data/verified_<lang>_overrides.json
    """

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        self.data_dir = data_dir or (REPO_ROOT / "multilingual" / "data")
        self._overrides: Dict[str, Dict[str, str]] = {}
        self._load_all_overrides()

    def _load_all_overrides(self) -> None:
        if not self.data_dir.exists():
            return

        # 1. Load primary verified Hindi overrides
        hi_legacy = self.data_dir / "verified_hi_overrides.json"
        if hi_legacy.exists():
            self._load_file("hi", hi_legacy)

        # 2. Load any per-language overrides in data/overrides/ or data/
        overrides_sub = self.data_dir / "overrides"
        if overrides_sub.exists() and overrides_sub.is_dir():
            for json_file in overrides_sub.glob("*.json"):
                lang_code = json_file.stem.lower()
                self._load_file(lang_code, json_file)

        for json_file in self.data_dir.glob("verified_*_overrides.json"):
            match = re.search(r"verified_([a-z]{2})_overrides\.json", json_file.name.lower())
            if match:
                lang_code = match.group(1)
                self._load_file(lang_code, json_file)

    def _load_file(self, lang_code: str, file_path: Path) -> None:
        try:
            with open(file_path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    if lang_code not in self._overrides:
                        self._overrides[lang_code] = {}
                    for k, v in data.items():
                        if isinstance(k, str) and isinstance(v, str):
                            self._overrides[lang_code][k.strip().lower()] = v.strip()
        except Exception:
            pass

    def get_translation(self, text: str, target_lang: str) -> Optional[str]:
        if not text or not target_lang:
            return None
        lang = target_lang.lower().strip()
        lang_dict = self._overrides.get(lang)
        if not lang_dict:
            return None

        clean_text = text.strip()
        lower_text = clean_text.lower()

        # Exact match (case-insensitive)
        if lower_text in lang_dict:
            return lang_dict[lower_text]

        # Punctuation stripped match
        stripped = re.sub(r"[^\w\s]", "", lower_text).strip()
        if stripped in lang_dict:
            return lang_dict[stripped]

        return None


# ─────────────────────────────────────────────────────────────────────────────
# 7. Offline Template & Regional Dictionary Provider (Tier 4 / Fallback)
# ─────────────────────────────────────────────────────────────────────────────

class OfflineTemplateProvider(BaseTranslationProvider):
    """Rule-based phrase and template translator that preserves numbers and units."""

    REGIONAL_DICTIONARY: Dict[str, Dict[str, str]] = {
        "hi": {
            "water footprint tracker": "जल पदचिह्न ट्रैकर",
            "search food items": "खाद्य पदार्थ खोजें",
            "water footprint": "जल पदचिह्न",
            "rice": "चावल", "wheat": "गेहूं", "apple": "सेब", "banana": "केला",
            "beef": "गोमांस", "chicken": "चिकन / मुर्गी", "milk": "दूध",
            "potato": "आलू", "tomato": "टमाटर", "coffee": "कॉफ़ी", "chocolate": "चॉकलेट",
            "almonds": "बादाम", "almond": "बादाम", "pork": "सूअर का मांस", "eggs": "अंडे",
            "cheese": "पनीर", "butter": "मक्खन", "bread": "रोटी / ब्रेड", "orange": "संतरा",
            "tea": "चाय", "sugar": "चीनी", "sugarcane": "गन्ना", "pulses": "दालें",
            "soybeans": "सोयाबीन", "corn": "मक्का", "maize": "मक्का", "cherry": "चेरी",
            "chilli": "मिर्च", "coconut": "नारियल", "cucumber": "खीरा", "jowar": "ज्वार",
            "lemon": "नींबू", "makhana": "मखाना", "papaya": "पपीता", "pearl_millet": "बाजरा",
            "pineapple": "अनानास", "pizza": "पिज़्ज़ा", "hamburger": "हैमबर्गर"
        },
        "mr": {
            "water footprint tracker": "पाण्याचा ठसा ट्रॅकर",
            "search food items": "अन्नपदार्थ शोधा",
            "water footprint": "पाण्याचा ठसा",
            "rice": "तांदूळ", "wheat": "गहू", "apple": "सफरचंद", "banana": "केळी",
            "beef": "गोमांस", "chicken": "चिकन", "milk": "दूध", "potato": "बटाटा",
            "tomato": "टोमॅटो", "coffee": "कॉफी", "chocolate": "चॉकलेट",
            "almonds": "बदाम", "pork": "डुकराचे मांस", "eggs": "अंडी",
            "cheese": "चीज", "butter": "लोणी", "bread": "पाव / ब्रेड", "orange": "संत्रे",
            "tea": "चहा", "sugar": "साखर", "sugarcane": "ऊस", "pulses": "कडधान्ये / डाळी",
            "soybeans": "सोयाबीन", "corn": "मका", "maize": "मका", "cherry": "चेरी",
            "chilli": "मिरची", "coconut": "नारळ", "cucumber": "काकडी", "jowar": "ज्वारी",
            "lemon": "लिंबू", "makhana": "मखाना", "papaya": "पपई", "pearl_millet": "बाजरी",
            "pineapple": "अननस"
        },
        "gu": {
            "water footprint tracker": "વોટર ફૂટપ્રિન્ટ ટ્રેકર",
            "search food items": "ખોરાકની વસ્તુઓ શોધો",
            "water footprint": "વોટર ફૂટપ્રિન્ટ",
            "rice": "ચોખા", "wheat": "ઘઉં", "apple": "સફરજન", "banana": "કેળા",
            "beef": "બીફ", "chicken": "ચિકન", "milk": "દૂધ", "potato": "બટાકા",
            "tomato": "ટમેટા", "coffee": "કોફી", "chocolate": "ચોકલેટ",
            "almonds": "બદામ", "pork": "ડુક્કરનું માંસ", "eggs": "ઇંડા",
            "cheese": "ચીઝ / પનીર", "butter": "માખણ", "bread": "રોટલી / બ્રેડ", "orange": "નારંગી",
            "tea": "ચા", "sugar": "ખાંડ", "sugarcane": "શેરડી", "pulses": "કઠોળ",
            "soybeans": "સોયાબીન", "corn": "મકાઈ", "maize": "મકાઈ", "cherry": "ચેરી",
            "chilli": "મરચું", "coconut": "નારિયેળ", "cucumber": "કાકડી", "jowar": "જુવાર",
            "lemon": "લીંબુ", "makhana": "મખાના", "papaya": "પપૈયું", "pearl_millet": "બાજરી",
            "pineapple": "અનાનસ"
        },
        "bn": {
            "water footprint tracker": "ওয়াটার ফুটপ্রিন্ট ট্র্যাকার",
            "search food items": "খাদ্যদ্রব্য অনুসন্ধান করুন",
            "water footprint": "পানির পদচিহ্ন",
            "rice": "চাল / ভাত", "wheat": "গম", "apple": "আপেল", "banana": "কলা",
            "beef": "গরুর মাংস", "chicken": "মুরগির মাংস", "milk": "দুধ", "potato": "আলু",
            "tomato": "টমেটো", "coffee": "কফি", "chocolate": "চকলেট",
            "almonds": "বাদাম", "pork": "শূকরের মাংস", "eggs": "ডিম",
            "cheese": "পনির", "butter": "মাখন", "bread": "রুটি / পাউরুটি", "orange": "কমলা",
            "tea": "চা", "sugar": "চিনি", "sugarcane": "আখ", "pulses": "ডাল",
            "soybeans": "সয়াবিন", "corn": "ভুট্টা", "maize": "ভুট্টা",
            "chilli": "মরিচ", "coconut": "নারকেল", "cucumber": "শসা", "jowar": "জোয়ার",
            "lemon": "লেবু", "papaya": "পেঁপে", "pearl_millet": "বাজরা", "pineapple": "আনারস"
        },
        "ta": {
            "water footprint tracker": "நீர் தடம் கண்காணிப்பாளர்",
            "search food items": "உணவு பொருட்களை தேடுங்கள்",
            "water footprint": "நீர் தடம்",
            "rice": "அரிசி", "wheat": "கோதுமை", "apple": "ஆப்பிள்", "banana": "வாழைப்பழம்",
            "beef": "மாட்டிறைச்சி", "chicken": "கோழிக்கறி", "milk": "பால்", "potato": "உருளைக்கிழங்கு",
            "tomato": "தக்காளி", "coffee": "காபி", "chocolate": "சாக்லேட்",
            "almonds": "பாதாம்", "eggs": "முட்டை", "cheese": "பாலாடைக்கட்டி",
            "butter": "வெண்ணெய்", "bread": "ரொட்டி", "orange": "ஆரஞ்சு",
            "tea": "தேநீர்", "sugar": "சர்க்கரை", "sugarcane": "கரும்பு", "pulses": "பருப்பு வகைகள்",
            "coconut": "தேங்காய்", "lemon": "எலுமிச்சை", "papaya": "பப்பாளி", "pineapple": "அன்னாசி"
        },
        "te": {
            "water footprint tracker": "నీటి పాదముద్ర ట్రాకర్",
            "search food items": "ఆహార పదార్థాలను శోధించండి",
            "water footprint": "నీటి పాదముద్ర",
            "rice": "వరి / బియ్యం", "wheat": "గోధుమలు", "apple": "ఆపిల్", "banana": "అరటిపండు",
            "beef": "గోమాంసం", "chicken": "చికెన్", "milk": "పాలు", "potato": "బంగాళాదుంప",
            "tomato": "టమోటా", "coffee": "కాఫీ", "chocolate": "చాక్లెట్",
            "almonds": "బాదం", "eggs": "గుడ్లు", "cheese": "జున్ను / పన్నీర్",
            "butter": "వెన్న", "bread": "రొట్టె / బ్రెడ్", "orange": "నారింజ",
            "tea": "టీ", "sugar": "చక్కెర", "sugarcane": "చెరకు", "pulses": "పప్పుధాన్యాలు",
            "coconut": "కొబ్బరికాయ", "lemon": "నిమ్మకాయ", "papaya": "బొప్పాయి", "pineapple": "అనాసపండు"
        },
        "kn": {
            "water footprint tracker": "ನೀರಿನ ಹೆಜ್ಜೆಗುರುತು ಟ್ರ್ಯಾಕರ್",
            "search food items": "ಆಹಾರ ಪದಾರ್ಥಗಳನ್ನು ಹುಡುಕಿ",
            "water footprint": "ನೀರಿನ ಹೆಜ್ಜೆಗುರುತು",
            "rice": "ಅಕ್ಕಿ / ಅನ್ನ", "wheat": "ಗೋಧಿ", "apple": "ಸೇಬು", "banana": "ಬಾಳೆಹಣ್ಣು",
            "chicken": "ಕೋಳಿ ಮಾಂಸ", "milk": "ಹಾಲು", "potato": "ಆಲೂಗಡ್ಡೆ",
            "tomato": "ಟೊಮೆಟೊ", "coffee": "ಕಾಫಿ", "chocolate": "ಚಾಕೊಲೇಟ್",
            "almonds": "ಬಾದಾಮಿ", "eggs": "ಮೊಟ್ಟೆಗಳು", "butter": "ಬೆಣ್ಣೆ", "bread": "ಬ್ರೆಡ್",
            "tea": "ಚಹಾ", "sugar": "ಸಕ್ಕರೆ", "sugarcane": "ಕಬ್ಬು", "pulses": "ಬೇಳೆಕಾಳುಗಳು",
            "coconut": "ತೆಂಗಿನಕಾಯಿ", "lemon": "ನಿಂಬೆ", "papaya": "ಪಪ್ಪಾಯಿ", "pineapple": "ಅನಾನಸ್"
        },
        "ml": {
            "water footprint tracker": "വാട്ടർ ഫുട്പ്രിന്റ് ട്രാക്കർ",
            "search food items": "ഭക്ഷണ സാധനങ്ങൾ തിരയുക",
            "water footprint": "ജല കാൽപ്പാട്",
            "rice": "അരി / ചോറ്", "wheat": "ഗോതമ്പ്", "apple": "ആപ്പിൾ", "banana": "വാഴപ്പഴം",
            "chicken": "ചിക്കൻ", "milk": "പാൽ", "potato": "ഉരുളക്കിഴങ്ങ്",
            "tomato": "തക്കാളി", "coffee": "കോഫി", "chocolate": "ചോക്ലേറ്റ്",
            "almonds": "ബദാം", "eggs": "മുട്ട", "butter": "വെണ്ണ", "bread": "റൊട്ടി",
            "tea": "ചായ", "sugar": "പഞ്ചസാര", "sugarcane": "കരിമ്പ്", "pulses": "പയറുവർഗ്ഗങ്ങൾ",
            "coconut": "തേങ്ങ", "lemon": "നാരങ്ങ", "papaya": "പപ്പായ", "pineapple": "കൈതച്ചക്ക"
        },
        "pa": {
            "water footprint tracker": "ਵਾਟਰ ਫੁੱਟਪ੍ਰਿੰਟ ਟਰੈਕਰ",
            "search food items": "ਭੋਜਨ ਪਦਾਰਥ ਖੋਜੋ",
            "water footprint": "ਜਲ ਪੈਰ-ਚਿੰਨ੍ਹ",
            "rice": "ਚੌਲ", "wheat": "ਕਣਕ", "apple": "ਸੇਬ", "banana": "ਕੇਲਾ",
            "chicken": "ਚਿਕਨ", "milk": "ਦੁੱਧ", "potato": "ਆਲੂ",
            "tomato": "ਟਮਾਟਰ", "coffee": "ਕੌਫੀ", "chocolate": "ਚਾਕਲੇਟ",
            "almonds": "ਬਦਾਮ", "eggs": "ਆਂਡੇ", "butter": "ਮੱਖਣ", "bread": "ਰੋਟੀ / ਬਰੈੱਡ",
            "tea": "ਚਾਹ", "sugar": "ਖੰਡ", "sugarcane": "ਗੰਨਾ", "pulses": "ਦਾਲਾਂ",
            "corn": "ਮੱਕੀ", "maize": "ਮੱਕੀ", "lemon": "ਨਿੰਬੂ", "papaya": "ਪਪੀਤਾ"
        }
    }

    BENCHMARK_UNITS: Dict[str, Dict[str, str]] = {
        "hi": {
            "bathtubs": "बाथटब", "bathtub": "बाथटब",
            "buckets": "बाल्टी", "bucket": "बाल्टी",
            "standard water bottles": "पानी की बोतलें", "standard water bottle": "पानी की बोतल",
            "showers": "शॉवर", "shower": "शॉवर",
            "swimming pools": "स्विमिंग पूल", "swimming pool": "स्विमिंग पूल",
            "glasses of water": "गिलास पानी", "glass of water": "गिलास पानी"
        },
        "mr": {
            "bathtubs": "बाथटब", "bathtub": "बाथटब",
            "buckets": "बादल्या", "bucket": "बादली",
            "standard water bottles": "पाण्याच्या बाटल्या", "standard water bottle": "पाण्याची बाटली",
            "showers": "शॉवर", "shower": "शॉवर",
            "swimming pools": "स्विमिंग पूल", "swimming pool": "स्विमिंग पूल"
        },
        "gu": {
            "bathtubs": "બાથટબ", "bathtub": "બાથટબ",
            "buckets": "ડોલ", "bucket": "ડોલ",
            "standard water bottles": "પાણીની બોટલો", "standard water bottle": "પાણીની બોટલ",
            "showers": "શાવર", "shower": "શાવર",
            "swimming pools": "સ્વિમિંગ પૂલ", "swimming pool": "સ્વિમિંગ પૂલ"
        },
        "bn": {
            "bathtubs": "বাথটাব", "bathtub": "বাথটাব",
            "buckets": "বালতি", "bucket": "বালতি",
            "standard water bottles": "পানির বোতল", "standard water bottle": "পানির বোতল",
            "showers": "শাওয়ার", "shower": "শাওয়ার",
            "swimming pools": "সুইমিং পুল", "swimming pool": "সুইমিং পুল"
        },
        "ta": {
            "bathtubs": "குளியல்தொட்டிகள்", "bathtub": "குளியல்தொட்டி",
            "buckets": "வாளிகள்", "bucket": "வாளி",
            "standard water bottles": "தண்ணீர் பாட்டில்கள்", "standard water bottle": "தண்ணீர் பாட்டில்",
            "showers": "குளியல்", "shower": "குளியல்",
            "swimming pools": "நீச்சல் குளங்கள்", "swimming pool": "நீச்சல் குளம்"
        },
        "te": {
            "bathtubs": "బాత్‌టబ్‌లు", "bathtub": "బాత్‌టబ్",
            "buckets": "బకెట్లు", "bucket": "బకెట్",
            "standard water bottles": "నీళ్ల సీసాలు", "standard water bottle": "నీళ్ల సీసా",
            "showers": "షవర్లు", "shower": "షవర్",
            "swimming pools": "ఈత కొలనులు", "swimming pool": "ఈత కొలను"
        },
        "kn": {
            "bathtubs": "ಬಾತ್‌ಟಬ್‌ಗಳು", "bathtub": "ಬಾತ್‌ಟಬ್",
            "buckets": "ಬಕೆಟ್‌ಗಳು", "bucket": "ಬಕೆಟ್",
            "showers": "ಶವರ್‌ಗಳು", "shower": "ಶವರ್",
            "swimming pools": "ಈಜುಕೊಳಗಳು", "swimming pool": "ಈಜುಕೊಳ"
        },
        "ml": {
            "bathtubs": "ബാത്ത് ടബ്ബുകൾ", "bathtub": "ബാത്ത് ടബ്ബ്",
            "buckets": "ബക്കറ്റുകൾ", "bucket": "ബക്കറ്റ്",
            "showers": "ഷവറുകൾ", "shower": "ഷവർ",
            "swimming pools": "നീന്തൽക്കുളങ്ങൾ", "swimming pool": "നീന്തൽക്കുളം"
        },
        "pa": {
            "bathtubs": "ਬਾਥਟੱਬ", "bathtub": "ਬਾਥਟੱਬ",
            "buckets": "ਬਾਲਟੀਆਂ", "bucket": "ਬਾਲਟੀ",
            "showers": "ਸ਼ਾਵਰ", "shower": "ਸ਼ਾਵਰ",
            "swimming pools": "ਸਵੀਮਿੰਗ ਪੂਲ", "swimming pool": "ਸਵੀਮਿੰਗ ਪੂਲ"
        }
    }

    def get_translation(self, text: str, target_lang: str) -> Optional[str]:
        if not text or not target_lang:
            return None
        lang = target_lang.lower().strip()
        clean_text = text.strip()
        lower_text = clean_text.lower()

        # 1. Direct dictionary match
        lang_dict = self.REGIONAL_DICTIONARY.get(lang, {})
        if lower_text in lang_dict:
            return lang_dict[lower_text]

        # 2. Benchmark template
        equiv_match = re.match(r"^equivalent to ~(\d+)\s+([a-zA-Z\s]+)\s+of water$", clean_text, re.IGNORECASE)
        if equiv_match:
            count = equiv_match.group(1)
            raw_unit = equiv_match.group(2).strip().lower()
            unit_map = self.BENCHMARK_UNITS.get(lang, {})
            translated_unit = unit_map.get(raw_unit, raw_unit)

            if lang == "hi":
                return f"लगभग {count} {translated_unit} पानी के बराबर"
            elif lang == "mr":
                return f"सुमारे {count} {translated_unit} पाण्यासमान"
            elif lang == "gu":
                return f"આશરે {count} {translated_unit} પાણી બરાબર"
            elif lang == "bn":
                return f"প্রায় {count} {translated_unit} পানির সমান"
            elif lang == "ta":
                return f"தோராயமாக {count} {translated_unit} தண்ணீருக்கு சமம்"
            elif lang == "te":
                return f"సుమారు {count} {translated_unit} నీటికి సమానం"
            elif lang == "kn":
                return f"ಸುಮಾರು {count} {translated_unit} ನೀರಿಗೆ ಸಮಾನ"
            elif lang == "ml":
                return f"ഏകദേശം {count} {translated_unit} വെള്ളത്തിന് തുല്യം"
            elif lang == "pa":
                return f"ਲਗਭਗ {count} {translated_unit} ਪਾਣੀ ਦੇ ਬਰਾਬਰ"
            else:
                return f"equivalent to ~{count} {translated_unit} of water"

        # 3. Standard seasonal produce advice
        if "conserve water by choosing locally grown, seasonal produce" in lower_text:
            tips = {
                "hi": "स्थानीय रूप से उगाए गए, मौसमी उत्पाद चुनकर जल संरक्षण करें।",
                "mr": "स्थानिक पातळीवर पिकवलेली, हंगामी उत्पादने निवडून पाण्याचे संवर्धन करा.",
                "gu": "સ્થાનિક રીતે ઉગાડવામાં આવેલ મોસમી ઉત્પાદનો પસંદ કરીને પાણીનું સંરક્ષણ કરો.",
                "bn": "স্থানীয়ভাবে উৎপাদিত, মৌসুমী পণ্য বেছে নিয়ে পানি সংরক্ষণ করুন।",
                "ta": "உள்ளூரில் விளையும் பருவகாலப் பொருட்களைத் தேர்ந்தெடுத்து தண்ணீரைச் சேமிக்கவும்.",
                "te": "స్థానికంగా పండించిన కాలానుగుణ ఉత్పత్తులను ఎంచుకోవడం ద్వారా నీటిని ఆదా చేయండి.",
                "kn": "ಸ್ಥಳೀಯವಾಗಿ ಬೆಳೆದ ಕಾಲೋಚಿತ ಉತ್ಪನ್ನಗಳನ್ನು ಆರಿಸುವ ಮೂಲಕ ನೀರನ್ನು ಉಳಿಸಿ.",
                "ml": "പ്രാദേശികമായി ഉൽപ്പാദിപ്പിക്കുന്ന ഉൽപ്പന്നങ്ങൾ തിരഞ്ഞെടുത്ത് വെള്ളം സംരക്ഷിക്കുക.",
                "pa": "ਸਥਾਨਕ ਤੌਰ 'ਤੇ ਉਗਾਈਆਂ ਗਈਆਂ ਮੌਸਮੀ ਵਸਤਾਂ ਦੀ ਚੋਣ ਕਰਕੇ ਪਾਣੀ ਦੀ ਬੱਚਤ ਕਰੋ।"
            }
            if lang in tips:
                return tips[lang]

        return None


# ─────────────────────────────────────────────────────────────────────────────
# 8. Pluggable External Translation Providers (Tier 4)
# ─────────────────────────────────────────────────────────────────────────────

class GoogleCloudTranslationProvider(BaseTranslationProvider):
    """Google Cloud Translation API v2 Provider.
    
    Reads credentials strictly from environment/configuration without hardcoding.
    Returns None if unconfigured or on network/API timeouts, gracefully delegating
    to offline providers.
    """

    def __init__(self, api_key: Optional[str] = None, timeout_seconds: float = 4.0) -> None:
        self.api_key = (
            api_key
            or os.getenv("GOOGLE_TRANSLATE_API_KEY")
            or os.getenv("TRANSLATE_API_KEY")
            or ""
        ).strip()
        self.timeout = timeout_seconds

    def get_translation(self, text: str, target_lang: str) -> Optional[str]:
        if not self.api_key or not text or target_lang in ("en", "english"):
            return None

        try:
            import urllib.request
            import urllib.parse

            url = f"https://translation.googleapis.com/language/translate/v2?key={self.api_key}"
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
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
                translations = data.get("data", {}).get("translations", [])
                if translations and "translatedText" in translations[0]:
                    return translations[0].get("translatedText")
        except Exception:
            # Gracefully handle network timeouts, HTTP errors, and API key issues
            pass
        return None


# Alias for backward compatibility
ExternalEngineProvider = GoogleCloudTranslationProvider


class BhashiniTranslationProvider(BaseTranslationProvider):
    """Pluggable provider interface for National Language Translation Mission (Bhashini / AI4Bharat).
    
    Configured via environment variables:
    - BHASHINI_USER_ID
    - BHASHINI_API_KEY
    - BHASHINI_PIPELINE_ID
    """

    def __init__(
        self,
        user_id: Optional[str] = None,
        api_key: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        timeout_seconds: float = 4.0,
    ) -> None:
        self.user_id = (user_id or os.getenv("BHASHINI_USER_ID") or "").strip()
        self.api_key = (api_key or os.getenv("BHASHINI_API_KEY") or "").strip()
        self.pipeline_id = (pipeline_id or os.getenv("BHASHINI_PIPELINE_ID") or "").strip()
        self.timeout = timeout_seconds

    def get_translation(self, text: str, target_lang: str) -> Optional[str]:
        if not self.api_key or not self.user_id or not text or target_lang == "en":
            return None
        # Pluggable interface implementation
        return None


class CompositeEngineProvider(BaseTranslationProvider):
    """Chains multiple translation engine providers and tries them sequentially."""

    def __init__(self, providers: Optional[List[BaseTranslationProvider]] = None) -> None:
        self.providers: List[BaseTranslationProvider] = providers or [
            GoogleCloudTranslationProvider(),
            BhashiniTranslationProvider(),
        ]

    def get_translation(self, text: str, target_lang: str) -> Optional[str]:
        for provider in self.providers:
            try:
                result = provider.get_translation(text, target_lang)
                if result:
                    return result
            except Exception:
                continue
        return None


def build_default_translation_provider() -> BaseTranslationProvider:
    """Builds the default configured translation provider chain."""
    return CompositeEngineProvider([
        GoogleCloudTranslationProvider(),
        BhashiniTranslationProvider(),
    ])


# ─────────────────────────────────────────────────────────────────────────────
# 9. Core Translation Service Orchestrator
# ─────────────────────────────────────────────────────────────────────────────

class TranslationService:
    """Orchestrates multi-tiered translation across verified glossary, verified sentences,
    cached translations, engine providers, and fallback layers.

    Resolution Priority:
    1. Verified agricultural glossary term (Highest Priority)
    2. Verified sentence translation / overrides
    3. Cached translation (L1 In-Memory / L2 Persistent SQLite)
    4. Translation-engine fallback (external API / Pluggable Provider Chain)
    5. Offline template & regional dictionary fallback
    6. English fallback (canonical source)
    """

    def __init__(
        self,
        cache_provider: Optional[BaseCacheProvider] = None,
        glossary_provider: Optional[BaseTranslationProvider] = None,
        verified_provider: Optional[BaseTranslationProvider] = None,
        engine_provider: Optional[BaseTranslationProvider] = None,
        template_provider: Optional[BaseTranslationProvider] = None,
    ) -> None:
        self.cache: BaseCacheProvider = cache_provider or HybridCacheProvider()
        self.glossary: BaseTranslationProvider = glossary_provider or GlossaryTranslationProvider()
        self.verified: BaseTranslationProvider = verified_provider or VerifiedTranslationProvider()
        self.engine: BaseTranslationProvider = engine_provider or build_default_translation_provider()
        self.template: BaseTranslationProvider = template_provider or OfflineTemplateProvider()

    def translate(self, text: str, target_language: str, source_language: str = "en") -> str:
        """Translates text to the target language following strict priority order:
        1. Verified glossary term (domain-specific terminology)
        2. Verified sentence translation (curated overrides)
        3. Cached translation (structured key: source_lang|text|target_lang)
        4. Translation-engine fallback (external API)
        5. Offline template & regional dictionary fallback
        6. English fallback (canonical source)
        
        Guarantees: Never raises exceptions, never crashes the API, preserves numbers and units.
        """
        if not text:
            return ""

        # Normalize target language code
        norm_code = normalize_language_code(target_language)
        if not norm_code or norm_code == "en":
            return text

        norm_src = normalize_language_code(source_language) or "en"
        clean_text = text.strip()

        # Step 1: Verified Agricultural Glossary Layer (Highest Priority)
        try:
            glossary_result = self.glossary.get_translation(clean_text, norm_code)
            if glossary_result:
                try:
                    self.cache.set(clean_text, norm_code, glossary_result, source_lang=norm_src)
                except Exception:
                    pass
                return glossary_result
        except Exception:
            pass

        # Step 2: Verified Sentence / Overrides Layer
        try:
            verified_result = self.verified.get_translation(clean_text, norm_code)
            if verified_result:
                try:
                    self.cache.set(clean_text, norm_code, verified_result, source_lang=norm_src)
                except Exception:
                    pass
                return verified_result
        except Exception:
            pass

        # Step 3: Structured Cache Layer (L1 Memory + L2 SQLite)
        try:
            cached_result = self.cache.get(clean_text, norm_code, source_lang=norm_src)
            if cached_result:
                return cached_result
        except Exception:
            pass

        # Step 4: Translation-Engine Layer (Cloud / External Pluggable Provider)
        try:
            engine_result = self.engine.get_translation(clean_text, norm_code)
            if engine_result:
                try:
                    self.cache.set(clean_text, norm_code, engine_result, source_lang=norm_src)
                except Exception:
                    pass
                return engine_result
        except Exception:
            pass

        # Step 5: Offline Template & Regional Dictionary Fallback
        try:
            template_result = self.template.get_translation(clean_text, norm_code)
            if template_result:
                try:
                    self.cache.set(clean_text, norm_code, template_result, source_lang=norm_src)
                except Exception:
                    pass
                return template_result
        except Exception:
            pass

        # Step 6: English Fallback (Canonical Source)
        return text


# Global Service Singleton
_service_instance: Optional[TranslationService] = None


def get_translation_service() -> TranslationService:
    """Returns the singleton instance of TranslationService."""
    global _service_instance
    if _service_instance is None:
        _service_instance = TranslationService()
    return _service_instance


def translate(text: str, target_language: str, source_language: str = "en") -> str:
    """Clean translation function."""
    return get_translation_service().translate(text, target_language, source_language=source_language)


def translate_text(text: str, target_lang: str = "en") -> str:
    """Backward-compatible wrapper for existing endpoints."""
    return translate(text, target_lang)
