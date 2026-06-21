from src.ai.llm_interface import LLMProvider
from src.config import get_settings

_instance: LLMProvider | None = None


def get_llm_provider() -> LLMProvider:
    global _instance
    if _instance is None:
        settings = get_settings()
        provider = settings.llm_provider.lower()
        if provider == "claude":
            from src.ai.providers.claude_provider import ClaudeProvider
            _instance = ClaudeProvider()
        elif provider == "azure_openai":
            from src.ai.providers.azure_openai_provider import AzureOpenAIProvider
            _instance = AzureOpenAIProvider()
        else:
            raise ValueError(f"Unknown LLM provider: {provider}. Set LLM_PROVIDER env var.")
    return _instance


def reset_provider() -> None:
    """For testing — reset singleton."""
    global _instance
    _instance = None
