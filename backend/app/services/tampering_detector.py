from PIL import Image, ImageChops, ImageEnhance
import numpy as np
from typing import Dict, Any
import os


class TamperingDetector:

    @staticmethod
    def run_ela(image_path: str, quality: int = 90) -> Dict[str, Any]:
        """
        Perform Error Level Analysis to detect tampering.
        """

        ela_image_path = image_path.replace(".", "_ela.")

        try:
            original = Image.open(image_path).convert("RGB")

            # Save temporary compressed image
            temp_path = image_path.replace(".", "_temp.")
            original.save(temp_path, "JPEG", quality=quality)

            compressed = Image.open(temp_path)

            # Compute difference
            diff = ImageChops.difference(original, compressed)

            extrema = diff.getextrema()
            max_diff = max([ex[1] for ex in extrema])

            scale = 255.0 / max_diff if max_diff != 0 else 1

            diff = ImageEnhance.Brightness(diff).enhance(scale)

            # Save ELA image
            ela_image_path = image_path.replace(".", "_ela.")
            diff.save(ela_image_path)

            # Convert to numpy to compute tampering score
            ela_array = np.array(diff)

            tampering_score = float(np.mean(ela_array) / 255)

            suspicious = tampering_score > 0.15

            # Cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            return {
                "tampering_score": round(tampering_score, 4),
                "suspicious": suspicious,
                "ela_image": ela_image_path
            }

        except Exception as e:
            return {
                "error": str(e),
                "suspicious": False
            }