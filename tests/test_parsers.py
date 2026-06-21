import pytest
from src.ingestion.parsers.markdown_parser import MarkdownParser
from src.ingestion.parsers.text_parser import TextParser
from src.ingestion.parsers.parser_factory import get_parser


def test_markdown_extracts_headings():
    content = b"# Title\n\nSome text\n\n## Section\n\nMore text"
    parser = MarkdownParser()
    result = parser.parse(content)
    assert len(result.pages) == 1
    assert "Title" in result.pages[0].headings
    assert "Section" in result.pages[0].headings
    assert "Some text" in result.pages[0].text


def test_text_parser():
    content = b"Hello world"
    parser = TextParser()
    result = parser.parse(content)
    assert result.pages[0].text == "Hello world"


def test_parser_factory_returns_correct_type():
    from src.ingestion.parsers.pdf_parser import PDFParser
    from src.ingestion.parsers.docx_parser import DocxParser
    assert isinstance(get_parser("pdf"), PDFParser)
    assert isinstance(get_parser("docx"), DocxParser)
    assert isinstance(get_parser("md"), MarkdownParser)
    assert isinstance(get_parser("txt"), TextParser)


def test_parser_factory_unknown():
    with pytest.raises(ValueError):
        get_parser("xyz")
