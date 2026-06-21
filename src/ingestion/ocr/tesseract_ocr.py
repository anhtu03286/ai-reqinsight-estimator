import io
import pytesseract
from PIL import Image
from src.config import get_settings
from .ocr_adapter import OCRAdapter


class TesseractOCR(OCRAdapter):
    def __init__(self):
        settings = get_settings()
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

    def extract_text(self, image_bytes: bytes) -> str:
        image = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(image, lang="eng+vie")


def ocr_pdf(pdf_bytes: bytes) -> str:
    """Convert PDF pages to images and run OCR on each."""
    import pdfplumber
    ocr = TesseractOCR()
    texts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            img = page.to_image(resolution=200)
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            text = ocr.extract_text(img_bytes.getvalue())
            texts.append(text)
    return "\n\n".join(texts)
