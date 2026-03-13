import exifread
from typing import Dict, Any


class MetadataAnalyzer:

    @staticmethod
    def analyze_metadata(image_path: str) -> Dict[str, Any]:
        """
        Analyze EXIF metadata to detect potential signs of editing.
        """

        result = {
            "metadata_present": False,
            "editing_software_detected": False,
            "software_name": None,
            "suspicious": False
        }

        try:
            with open(image_path, "rb") as f:
                tags = exifread.process_file(f)

            if tags:
                result["metadata_present"] = True

                # Check for software tag (editing programs leave this)
                if "Image Software" in tags:
                    result["editing_software_detected"] = True
                    result["software_name"] = str(tags["Image Software"])
                    result["suspicious"] = True

        except Exception as e:
            result["error"] = str(e)

        return result