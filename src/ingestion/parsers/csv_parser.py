import io
import csv
from .base import BaseParser, ParseResult, ParsedPage


class CSVParser(BaseParser):
    def parse(self, content: bytes) -> ParseResult:
        text = content.decode("utf-8", errors="replace")
        dialect = csv.Sniffer().sniff(text[:4096], delimiters=",;\t")
        reader = csv.reader(io.StringIO(text), dialect)
        rows = list(reader)
        if not rows:
            return ParseResult(pages=[ParsedPage(page=1, text="", headings=[])])

        headers = rows[0]
        lines = [" | ".join(headers)]
        for row in rows[1:]:
            lines.append(" | ".join(str(c) for c in row))

        return ParseResult(pages=[ParsedPage(page=1, text="\n".join(lines), headings=headers)])
