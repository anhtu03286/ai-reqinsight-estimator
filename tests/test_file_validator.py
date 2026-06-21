import io
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.ingestion.validators.file_validator import validate_file, validate_file_size
from src.models.document import MAX_FILE_SIZE_BYTES


def _make_upload(filename: str, content: bytes = b"data"):
    f = MagicMock()
    f.filename = filename
    f.content_type = "application/octet-stream"
    f.read = MagicMock(return_value=content)
    return f


def test_validate_file_allowed():
    for ext in ["pdf", "docx", "md", "txt", "xlsx", "csv"]:
        f = _make_upload(f"file.{ext}")
        result = validate_file(f)
        assert result == ext


def test_validate_file_rejected():
    f = _make_upload("file.exe")
    with pytest.raises(HTTPException) as exc:
        validate_file(f)
    assert exc.value.status_code == 400
    assert "UNSUPPORTED_FORMAT" in str(exc.value.detail)


@pytest.mark.asyncio
async def test_file_size_ok():
    f = _make_upload("ok.pdf", b"x" * 100)
    f.read = MagicMock(return_value=b"x" * 100)

    async def async_read():
        return b"x" * 100

    f.read = async_read
    content = await validate_file_size(f)
    assert len(content) == 100


@pytest.mark.asyncio
async def test_file_size_too_large():
    big = b"x" * (MAX_FILE_SIZE_BYTES + 1)
    f = MagicMock()
    f.filename = "big.pdf"

    async def async_read():
        return big

    f.read = async_read
    with pytest.raises(HTTPException) as exc:
        await validate_file_size(f)
    assert exc.value.status_code == 400
    assert "DOCUMENT_TOO_LARGE" in str(exc.value.detail)
