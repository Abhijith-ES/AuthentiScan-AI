import os
from dotenv import load_dotenv
import pytesseract

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

UPLOAD_FOLDER = "backend/uploads"

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]