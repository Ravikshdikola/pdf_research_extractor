import fitz  # PyMuPDF
from PIL import Image
import io
import pytesseract
import logging

def pdf_to_text(pdf_path: str) -> str:
    """Extract text from PDF using PyMuPDF and OCR (Tesseract)."""
    try:
        doc = fitz.open(pdf_path)
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=600)
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(image)
            full_text += text + "\n"
        return full_text
    except Exception as e:
        logging.error(f"Error during OCR extraction: {e}")
        raise
