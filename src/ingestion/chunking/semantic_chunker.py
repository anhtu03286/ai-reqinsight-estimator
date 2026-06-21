import re
import tiktoken
from dataclasses import dataclass

MAX_TOKENS = 500
OVERLAP_TOKENS = 50
ENCODING = "cl100k_base"


@dataclass
class Chunk:
    chunk_index: int
    content: str
    page_number: int | None
    section_header: str | None
    token_count: int


def _count_tokens(text: str, enc) -> int:
    return len(enc.encode(text))


def _split_sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?])\s+", text.strip())


def chunk_document(pages: list[dict]) -> list[Chunk]:
    """
    pages: list of {"page": int, "text": str, "headings": list[str]}
    Returns chunks with overlap, not cutting sentences.
    """
    enc = tiktoken.get_encoding(ENCODING)
    chunks: list[Chunk] = []
    chunk_index = 0
    current_section = None

    for page_data in pages:
        page_num = page_data.get("page", 1)
        headings = page_data.get("headings", [])
        text = page_data.get("text", "").strip()

        if headings:
            current_section = headings[0]

        sentences = _split_sentences(text)
        current_tokens: list[str] = []
        current_token_count = 0

        for sentence in sentences:
            sentence_tokens = enc.encode(sentence)
            if current_token_count + len(sentence_tokens) > MAX_TOKENS and current_tokens:
                chunk_text = enc.decode(current_tokens)
                chunks.append(Chunk(
                    chunk_index=chunk_index,
                    content=chunk_text,
                    page_number=page_num,
                    section_header=current_section,
                    token_count=current_token_count,
                ))
                chunk_index += 1
                # Overlap: keep last OVERLAP_TOKENS tokens
                overlap = current_tokens[-OVERLAP_TOKENS:] if len(current_tokens) > OVERLAP_TOKENS else current_tokens[:]
                current_tokens = overlap + sentence_tokens
                current_token_count = len(current_tokens)
            else:
                current_tokens.extend(sentence_tokens)
                current_token_count += len(sentence_tokens)

        if current_tokens:
            chunk_text = enc.decode(current_tokens)
            chunks.append(Chunk(
                chunk_index=chunk_index,
                content=chunk_text,
                page_number=page_num,
                section_header=current_section,
                token_count=current_token_count,
            ))
            chunk_index += 1

    return chunks
