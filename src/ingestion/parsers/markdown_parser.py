import re
from .base import BaseParser, ParseResult, ParsedPage

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


class MarkdownParser(BaseParser):
    def parse(self, content: bytes) -> ParseResult:
        text = content.decode("utf-8", errors="replace")
        headings = [m.group(2).strip() for m in HEADING_RE.finditer(text)]
        return ParseResult(pages=[ParsedPage(page=1, text=text, headings=headings)])
