import io
import pdfplumber
from .base import BaseParser, ParseResult, ParsedPage


class PDFParser(BaseParser):
    def parse(self, content: bytes) -> ParseResult:
        pages = []
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                headings = self._extract_headings(page)
                pages.append(ParsedPage(page=i, text=text, headings=headings))

        total_text = " ".join(p.text for p in pages).strip()
        needs_ocr = len(total_text) < 50  # likely scanned if very little text
        return ParseResult(pages=pages, needs_ocr=needs_ocr)

    def _extract_headings(self, page) -> list[str]:
        headings = []
        if not page.chars:
            return headings
        # Heuristic: large font size chars at line start = heading
        try:
            avg_size = sum(c.get("size", 12) for c in page.chars) / max(len(page.chars), 1)
            seen = set()
            for char in page.chars:
                if char.get("size", 12) > avg_size * 1.3:
                    # Group into words by line
                    line_key = round(char.get("top", 0))
                    if line_key not in seen:
                        seen.add(line_key)
                        headings.append(char.get("text", "").strip())
        except Exception:
            pass
        return [h for h in headings if h]
