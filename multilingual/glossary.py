"""Verified Agricultural and Scientific Terminology Glossary System."""

import json
from pathlib import Path
from typing import Dict, List, Optional

GLOSSARY_FILE = Path(__file__).resolve().parent / "data" / "glossary.json"


class AgriculturalGlossary:
    """Provides verified domain-specific terminology lookups across languages.
    
    Structure: language_code -> canonical_term (lowercase) -> verified_translation
    """

    def __init__(self, json_path: Path = GLOSSARY_FILE) -> None:
        self._glossary: Dict[str, Dict[str, str]] = {}
        self._canonical_terms: set[str] = set()
        self._load(json_path)

    def _load(self, path: Path) -> None:
        if not path.exists():
            return
        try:
            with open(path, mode="r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                for lang, terms in data.items():
                    lang_code = lang.strip().lower()
                    if lang_code not in self._glossary:
                        self._glossary[lang_code] = {}
                    for term, trans in terms.items():
                        clean_term = term.strip().lower()
                        self._glossary[lang_code][clean_term] = trans.strip()
                        self._canonical_terms.add(clean_term)
        except Exception:
            pass

    def get_term(self, term: str, target_lang: str) -> Optional[str]:
        """Looks up a verified glossary translation for a given canonical agricultural term."""
        if not term or not target_lang:
            return None
        lang = target_lang.strip().lower()
        clean_term = term.strip().lower()
        return self._glossary.get(lang, {}).get(clean_term)

    def get_all_terms(self, target_lang: str) -> Dict[str, str]:
        """Returns all verified glossary terms available for a specific language."""
        lang = target_lang.strip().lower()
        return dict(self._glossary.get(lang, {}))

    def get_canonical_terms(self) -> List[str]:
        """Returns the list of all canonical English glossary terms."""
        return sorted(list(self._canonical_terms))

    def has_term(self, term: str) -> bool:
        """Checks if a term exists in the canonical glossary index."""
        return term.strip().lower() in self._canonical_terms


# Singleton instance
glossary = AgriculturalGlossary()


def get_glossary_translation(term: str, target_lang: str) -> Optional[str]:
    """Retrieves verified agricultural terminology translation."""
    return glossary.get_term(term, target_lang)


def get_all_glossary_terms(target_lang: str) -> Dict[str, str]:
    """Retrieves all verified terms for a given language."""
    return glossary.get_all_terms(target_lang)


def get_canonical_glossary_terms() -> List[str]:
    """Returns canonical glossary terms."""
    return glossary.get_canonical_terms()
