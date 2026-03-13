import pytesseract
import cv2
import numpy as np
from typing import Dict, Any


class OCRExtractor:

    @staticmethod
    def extract_text(image_path: str) -> Dict[str, Any]:
        """
        Extract text from ID document using Tesseract OCR.
        """

        try:
            # Load image using OpenCV
            image = cv2.imread(image_path)

            if image is None:
                return {
                    "success": False,
                    "reason": "Unable to load image for OCR"
                }

            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Noise reduction
            gray = cv2.medianBlur(gray, 3)

            # Thresholding improves OCR
            thresh = cv2.threshold(
                gray,
                0,
                255,
                cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]

            # Run OCR
            text = pytesseract.image_to_string(thresh)

            # Clean extracted text
            cleaned_text = text.strip()

            return {
                "success": True,
                "extracted_text": cleaned_text,
                "text_length": len(cleaned_text)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }