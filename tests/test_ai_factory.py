import pytest
from unittest.mock import patch, MagicMock
from src.ai.ai_factory import get_llm_provider, reset_provider


def test_factory_returns_claude_by_default():
    reset_provider()
    with patch("src.config.get_settings") as mock_settings:
        s = MagicMock()
        s.llm_provider = "claude"
        s.anthropic_api_key = "test"
        mock_settings.return_value = s

        with patch("src.ai.providers.claude_provider.anthropic.Anthropic"):
            from src.ai.ai_factory import get_llm_provider, reset_provider
            reset_provider()
            provider = get_llm_provider()
            from src.ai.providers.claude_provider import ClaudeProvider
            assert isinstance(provider, ClaudeProvider)
    reset_provider()


def test_factory_raises_for_unknown_provider():
    reset_provider()
    with patch("src.config.get_settings") as mock_settings:
        s = MagicMock()
        s.llm_provider = "unknown_provider"
        mock_settings.return_value = s
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            get_llm_provider()
    reset_provider()
