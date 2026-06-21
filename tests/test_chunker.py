import pytest
from src.ingestion.chunking.semantic_chunker import chunk_document


def test_single_short_page():
    pages = [{"page": 1, "text": "Hello world. This is a test.", "headings": ["Intro"]}]
    chunks = chunk_document(pages)
    assert len(chunks) == 1
    assert chunks[0].section_header == "Intro"
    assert chunks[0].page_number == 1
    assert "Hello" in chunks[0].content


def test_long_text_splits_into_multiple_chunks():
    sentence = "This is a sentence with enough words to consume tokens. " * 30
    pages = [{"page": 1, "text": sentence, "headings": []}]
    chunks = chunk_document(pages)
    assert len(chunks) >= 2


def test_overlap_maintains_context():
    sentences = ["Sentence number {}.".format(i) for i in range(100)]
    text = " ".join(sentences)
    pages = [{"page": 1, "text": text, "headings": []}]
    chunks = chunk_document(pages)
    # Check that consecutive chunks share some content (overlap)
    if len(chunks) >= 2:
        words_in_1 = set(chunks[0].content.split())
        words_in_2 = set(chunks[1].content.split())
        assert len(words_in_1 & words_in_2) > 0


def test_chunk_indices_are_sequential():
    pages = [{"page": i, "text": f"Page {i} content." * 20, "headings": []} for i in range(1, 4)]
    chunks = chunk_document(pages)
    for i, chunk in enumerate(chunks):
        assert chunk.chunk_index == i


def test_empty_input():
    assert chunk_document([]) == []
