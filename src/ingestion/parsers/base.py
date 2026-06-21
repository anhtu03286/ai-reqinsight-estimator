from dataclasses import dataclass, field
from abc import ABC, abstractmethod


@dataclass
class ParsedPage:
    page: int
    text: str
    headings: list[str] = field(default_factory=list)


@dataclass
class ParseResult:
    pages: list[ParsedPage]
    needs_ocr: bool = False
    detected_language: str | None = None


class BaseParser(ABC):
    @abstractmethod
    def parse(self, content: bytes) -> ParseResult:
        pass
