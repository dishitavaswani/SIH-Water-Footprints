"""Unit tests for Step 7: Pluggable Translation Provider Architecture."""

import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from backend.app.services.translation_service import (
    BaseTranslationProvider,
    GoogleCloudTranslationProvider,
    BhashiniTranslationProvider,
    CompositeEngineProvider,
    InMemoryCacheProvider,
    TranslationService,
    build_default_translation_provider,
)


class MockExternalProvider(BaseTranslationProvider):
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.call_history = []

    def get_translation(self, text: str, target_lang: str):
        self.call_history.append((text, target_lang))
        return self.responses.get((text.strip().lower(), target_lang.strip().lower()))


class CrashingTimeoutProvider(BaseTranslationProvider):
    def get_translation(self, text: str, target_lang: str):
        raise TimeoutError("External API request timed out after 4000ms")


class TestPluggableTranslationProviderStep7(unittest.TestCase):
    def setUp(self):
        self.target_languages = ["hi", "mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]

    def test_unconfigured_providers_return_none_safely(self):
        """When credentials are not present in env, providers must return None without raising errors."""
        with patch.dict(os.environ, {}, clear=True):
            google_provider = GoogleCloudTranslationProvider(api_key="")
            self.assertIsNone(google_provider.get_translation("Hello", "hi"))

            bhashini_provider = BhashiniTranslationProvider(api_key="", user_id="")
            self.assertIsNone(bhashini_provider.get_translation("Hello", "mr"))

            composite = CompositeEngineProvider([google_provider, bhashini_provider])
            self.assertIsNone(composite.get_translation("Hello", "gu"))

    def test_custom_mock_provider_plugs_into_translation_service(self):
        """TranslationService must work seamlessly with any injected BaseTranslationProvider."""
        mock_responses = {
            ("organic tomato", "mr"): "सेंद्रिय टोमॅटो",
            ("organic tomato", "gu"): "ઓર્ગેનિક ટામેટા",
            ("organic tomato", "bn"): "জৈব টমেটো",
            ("organic tomato", "ta"): "இயற்கை தக்காளி",
            ("organic tomato", "te"): "సేంద్రీయ టమోటా",
            ("organic tomato", "kn"): "ಸಾವಯವ ಟೊಮೆಟೊ",
            ("organic tomato", "ml"): "ഓർഗാനിക് തക്കാളി",
            ("organic tomato", "pa"): "ਜੈਵਿਕ ਟਮਾਟਰ",
        }
        mock_provider = MockExternalProvider(mock_responses)
        cache = InMemoryCacheProvider()

        service = TranslationService(
            cache_provider=cache,
            glossary_provider=MockExternalProvider({}),
            verified_provider=MockExternalProvider({}),
            engine_provider=mock_provider,
            template_provider=MockExternalProvider({}),
        )

        for lang in ["mr", "gu", "bn", "ta", "te", "kn", "ml", "pa"]:
            translated = service.translate("organic tomato", lang)
            self.assertEqual(
                translated,
                mock_responses[("organic tomato", lang)],
                f"Translation failed for {lang}",
            )

    def test_provider_timeout_falls_back_gracefully_to_english(self):
        """When external provider times out or crashes, the application must return fallback gracefully."""
        crashing_provider = CrashingTimeoutProvider()
        cache = InMemoryCacheProvider()

        service = TranslationService(
            cache_provider=cache,
            glossary_provider=MockExternalProvider({}),
            verified_provider=MockExternalProvider({}),
            engine_provider=crashing_provider,
            template_provider=MockExternalProvider({}),
        )

        # Must NOT raise TimeoutError; must fallback to English safely
        result = service.translate("Resilient Fallback Phrase", "ta")
        self.assertEqual(result, "Resilient Fallback Phrase")

    def test_composite_provider_chains_backup_on_failure(self):
        """If primary provider returns None or fails, composite provider delegates to secondary."""
        provider_a = CrashingTimeoutProvider()
        provider_b = MockExternalProvider({("dragon fruit", "hi"): "ड्रैगन फ्रूट"})

        composite = CompositeEngineProvider([provider_a, provider_b])
        result = composite.get_translation("dragon fruit", "hi")
        self.assertEqual(result, "ड्रैगन फ्रूट")

    def test_complete_resolution_priority_chain(self):
        """Strict resolution priority: Glossary > Sentence Override > Cache > External Engine > English."""
        glossary_mock = MockExternalProvider({("priority test", "mr"): "शब्दावली (Glossary)"})
        sentence_mock = MockExternalProvider({("priority test", "mr"): "वाक्य (Sentence)"})
        engine_mock = MockExternalProvider({("priority test", "mr"): "इंजिन (Engine)"})

        # 1. Glossary takes priority over all
        cache1 = InMemoryCacheProvider()
        svc1 = TranslationService(
            cache_provider=cache1,
            glossary_provider=glossary_mock,
            verified_provider=sentence_mock,
            engine_provider=engine_mock,
            template_provider=MockExternalProvider({}),
        )
        self.assertEqual(svc1.translate("priority test", "mr"), "शब्दावली (Glossary)")

        # 2. When glossary is empty, Sentence takes priority over engine & cache
        cache2 = InMemoryCacheProvider()
        cache2.set("priority test", "mr", "कॅश (Cache)")
        svc2 = TranslationService(
            cache_provider=cache2,
            glossary_provider=MockExternalProvider({}),
            verified_provider=sentence_mock,
            engine_provider=engine_mock,
            template_provider=MockExternalProvider({}),
        )
        self.assertEqual(svc2.translate("priority test", "mr"), "वाक्य (Sentence)")

        # 3. When verified is empty, Cache takes priority over engine
        cache3 = InMemoryCacheProvider()
        cache3.set("priority test", "mr", "कॅश (Cache)")
        svc3 = TranslationService(
            cache_provider=cache3,
            glossary_provider=MockExternalProvider({}),
            verified_provider=MockExternalProvider({}),
            engine_provider=engine_mock,
            template_provider=MockExternalProvider({}),
        )
        self.assertEqual(svc3.translate("priority test", "mr"), "कॅश (Cache)")

        # 4. When cache is empty, Engine is called
        cache4 = InMemoryCacheProvider()
        svc4 = TranslationService(
            cache_provider=cache4,
            glossary_provider=MockExternalProvider({}),
            verified_provider=MockExternalProvider({}),
            engine_provider=engine_mock,
            template_provider=MockExternalProvider({}),
        )
        self.assertEqual(svc4.translate("priority test", "mr"), "इंजिन (Engine)")


if __name__ == "__main__":
    unittest.main()
