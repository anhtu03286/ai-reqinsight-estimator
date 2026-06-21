from src.ai.llm_interface import LLMProvider, AnalysisResponse


class AzureOpenAIProvider(LLMProvider):
    """Stub — implement when Azure OpenAI contract is confirmed."""

    def analyze(self, prompt: str, context_chunks: list[str]) -> AnalysisResponse:
        raise NotImplementedError("AzureOpenAIProvider not implemented yet")

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError("AzureOpenAIProvider not implemented yet")

    def chat(self, messages: list[dict]) -> str:
        raise NotImplementedError("AzureOpenAIProvider not implemented yet")
