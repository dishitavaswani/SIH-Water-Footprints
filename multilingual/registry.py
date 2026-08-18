"""Centralized language registry for the multilingual system."""

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional

REGISTRY_FILE = Path(__file__).resolve().parent / "languages.json"


@dataclass(frozen=True)
class LanguageInfo:
    code: str
    name: str
    native_name: str
    is_verified: bool
    offline_fallback: bool

    def to_dict(self) -> Dict[str, any]:
        return asdict(self)


class LanguageRegistry:
    """Single source of truth for supported languages across backend and clients."""

    def __init__(self, json_path: Path = REGISTRY_FILE):
        self._languages: Dict[str, LanguageInfo] = {}
        self._name_alias_map: Dict[str, str] = {}
        self._load_from_json(json_path)

    def _load_from_json(self, path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(f"Language registry file not found at: {path}")

        with open(path, mode="r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data.get("languages", []):
            info = LanguageInfo(
                code=item["code"].strip().lower(),
                name=item["name"].strip(),
                native_name=item["native_name"].strip(),
                is_verified=bool(item.get("is_verified", False)),
                offline_fallback=bool(item.get("offline_fallback", False)),
            )
            self._languages[info.code] = info
            # Alias mappings for common full names (e.g. 'hindi' -> 'hi', 'english' -> 'en')
            self._name_alias_map[info.name.lower()] = info.code
            self._name_alias_map[info.native_name.lower()] = info.code

    def get_all(self) -> List[LanguageInfo]:
        """Returns all registered languages in canonical order."""
        return list(self._languages.values())

    def get_codes(self) -> List[str]:
        """Returns list of supported ISO language codes."""
        return list(self._languages.keys())

    def get_language(self, code_or_name: str) -> Optional[LanguageInfo]:
        """Looks up a language by ISO code or standard alias."""
        if not code_or_name:
            return None
        clean = code_or_name.strip().lower()
        if clean in self._languages:
            return self._languages[clean]
        resolved_code = self._name_alias_map.get(clean)
        if resolved_code and resolved_code in self._languages:
            return self._languages[resolved_code]
        return None

    def is_supported(self, code_or_name: str) -> bool:
        """Checks whether a language is supported in the registry."""
        return self.get_language(code_or_name) is not None

    def normalize_code(self, code_or_name: str) -> Optional[str]:
        """Normalizes a language input (e.g., 'Hindi', 'hi', 'HI') to its standard code ('hi')."""
        lang = self.get_language(code_or_name)
        return lang.code if lang else None


# Module singleton instance
registry = LanguageRegistry()


def get_supported_languages() -> List[Dict[str, any]]:
    """Returns serialized list of supported language dictionaries."""
    return [lang.to_dict() for lang in registry.get_all()]


def get_supported_codes() -> List[str]:
    """Returns list of supported language codes."""
    return registry.get_codes()


def is_supported_language(code_or_name: str) -> bool:
    """Returns True if code/name is in the supported language registry."""
    return registry.is_supported(code_or_name)


def normalize_language_code(code_or_name: str) -> Optional[str]:
    """Returns canonical language code or None if unsupported."""
    return registry.normalize_code(code_or_name)


def get_language_info(code_or_name: str) -> Optional[Dict[str, any]]:
    """Returns language info dict or None if unsupported."""
    lang = registry.get_language(code_or_name)
    return lang.to_dict() if lang else None
