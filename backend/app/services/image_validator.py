import os
from fastapi import UploadFile
from PIL import Image
from typing import Dict, Any
from backend.app.core.config import ALLOWED_IMAGE_TYPES


class ImageValidator:

    @staticmethod
    async def validate_image(file: UploadFile) -> Dict[str, Any]:
        """
        Validate uploaded image file.
        Returns validation result and loaded image.
        """

        # Step 1: Check MIME type
        if file.content_type not in ALLOWED_IMAGE_TYPES:
            return {
                "valid": False,
                "reason": "Unsupported file type"
            }

        # Step 2: Read file bytes
        contents = await file.read()

        # Step 3: Save temporarily
        temp_path = f"backend/uploads/{file.filename}"

        with open(temp_path, "wb") as f:
            f.write(contents)

        # Step 4: Check if image can be opened
        try:
            img = Image.open(temp_path)
            img.verify()  # Detect corruption
        except Exception:
            return {
                "valid": False,
                "reason": "Corrupted or unreadable image"
            }

        # Step 5: Re-open image after verify
        img = Image.open(temp_path)

        return {
            "valid": True,
            "path": temp_path,
            "image": img
        }