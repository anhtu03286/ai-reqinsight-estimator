from fastapi import HTTPException, status, UploadFile
from src.models.document import ALLOWED_FORMATS, MAX_FILE_SIZE_BYTES
import os


def validate_file(file: UploadFile) -> str:
    ext = os.path.splitext(file.filename or "")[1].lstrip(".").lower()
    if ext not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "UNSUPPORTED_FORMAT", "message": f"Format '{ext}' is not supported"},
        )
    return ext


async def validate_file_size(file: UploadFile) -> bytes:
    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "DOCUMENT_TOO_LARGE", "message": "File exceeds 50MB limit"},
        )
    return content
