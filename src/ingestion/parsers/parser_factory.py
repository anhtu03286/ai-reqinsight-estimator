from .base import BaseParser
from .pdf_parser import PDFParser
from .docx_parser import DocxParser
from .markdown_parser import MarkdownParser
from .text_parser import TextParser
from .excel_parser import ExcelParser
from .csv_parser import CSVParser


_PARSERS: dict[str, type[BaseParser]] = {
    "pdf": PDFParser,
    "docx": DocxParser,
    "doc": DocxParser,
    "md": MarkdownParser,
    "txt": TextParser,
    "xlsx": ExcelParser,
    "xls": ExcelParser,
    "csv": CSVParser,
}


def get_parser(fmt: str) -> BaseParser:
    parser_cls = _PARSERS.get(fmt.lower())
    if not parser_cls:
        raise ValueError(f"No parser for format: {fmt}")
    return parser_cls()
