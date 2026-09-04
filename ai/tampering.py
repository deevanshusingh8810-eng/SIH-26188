from PIL import Image, ImageChops, ImageEnhance
import os


def detect_tampering(file_path):

    # PDFs are not handled by this basic image tampering detector
    if file_path.lower().endswith(".pdf"):
        return {
            "tampering_score": 0,
            "suspicious": False,
            "details": ["Tampering analysis currently supports image files only"]
        }

    try:
        image = Image.open(file_path).convert("RGB")

        width, height = image.size

        issues = []
        score = 0

        # Check for very low resolution
        if width < 500 or height < 500:
            score += 20
            issues.append("Low resolution document image")

        # Check whether the image contains an unusual amount of compression artifacts
        enhanced = ImageEnhance.Contrast(image).enhance(2)
        difference = ImageChops.difference(image, enhanced)

        # Get bounding box of differences
        bbox = difference.getbbox()

        if bbox is None:
            issues.append("Image has very low visual variation")

        suspicious = score >= 30

        return {
            "tampering_score": score,
            "suspicious": suspicious,
            "details": issues
        }

    except Exception as e:
        return {
            "tampering_score": 50,
            "suspicious": True,
            "details": [f"Tampering analysis error: {str(e)}"]
        }
