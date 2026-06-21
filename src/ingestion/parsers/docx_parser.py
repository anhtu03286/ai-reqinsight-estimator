import io
from docx import Document as DocxDocument
from .base import BaseParser, ParseResult, ParsedPage

HEADING_STYLES = {"Heading 1", "Heading 2", "Heading 3", "Title"}


class DocxParser(BaseParser):
    def parse(self, content: bytes) -> ParseResult:
        doc = DocxDocument(io.BytesIO(content))
        headings = []
        all_text_lines = []

        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            if para.style and para.style.name in HEADING_STYLES:
                headings.append(text)
            all_text_lines.append(text)

        full_text = "\n".join(all_text_lines)
        return ParseResult(
            pages=[ParsedPage(page=1, text=full_text, headings=headings)]
        )
