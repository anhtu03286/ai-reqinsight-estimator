from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AnalysisResponse:
    results: list[dict]  # list of {type, severity, title, content, chunk_id}
    model_version: str


class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, prompt: str, context_chunks: list[str]) -> AnalysisResponse:
        pass

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        pass

    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        pass
