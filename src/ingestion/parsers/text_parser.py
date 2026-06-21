from .base import BaseParser, ParseResult, ParsedPage


class TextParser(BaseParser):
    def parse(self, content: bytes) -> ParseResult:
        text = content.decode("utf-8", errors="replace")
        return ParseResult(pages=[ParsedPage(page=1, text=text, headings=[])])
