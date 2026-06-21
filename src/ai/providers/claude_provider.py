import json
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from src.ai.llm_interface import LLMProvider, AnalysisResponse
from src.config import get_settings

settings = get_settings()
MODEL = "claude-sonnet-4-6"
EMBED_MODEL = "voyage-3"  # Anthropic recommends Voyage for embeddings


class ClaudeProvider(LLMProvider):
    def __init__(self):
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    @retry(
        retry=retry_if_exception_type((anthropic.APIConnectionError, anthropic.RateLimitError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def analyze(self, prompt: str, context_chunks: list[str]) -> AnalysisResponse:
        context = "\n\n---\n\n".join(context_chunks[:20])  # cap context
        message = self._client.messages.create(
            model=MODEL,
            max_tokens=4096,
            timeout=60,
            messages=[{"role": "user", "content": f"{prompt}\n\nDocument content:\n{context}"}],
        )
        raw = message.content[0].text
        try:
            parsed = json.loads(raw)
            results = parsed.get("results", [])
        except json.JSONDecodeError:
            results = []
        return AnalysisResponse(results=results, model_version=MODEL)

    def embed(self, text: str) -> list[float]:
        try:
            import voyageai
            key = settings.voyage_api_key or settings.anthropic_api_key
            vo = voyageai.Client(api_key=key)
            result = vo.embed([text], model="voyage-3")
            return result.embeddings[0]
        except Exception:
            return [0.0] * 1536

    @retry(
        retry=retry_if_exception_type((anthropic.APIConnectionError, anthropic.RateLimitError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=30),
    )
    def chat(self, messages: list[dict]) -> str:
        response = self._client.messages.create(
            model=MODEL,
            max_tokens=2048,
            timeout=60,
            messages=messages,
        )
        return response.content[0].text
