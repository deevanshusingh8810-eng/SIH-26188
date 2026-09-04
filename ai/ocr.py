import pytesseract
from PIL import Image, ImageOps, ImageEnhance


def run_ocr(file_path):
    try:
        image = Image.open(file_path)

        # Convert to grayscale
        image = ImageOps.grayscale(image)

        # Improve contrast
        image = ImageEnhance.Contrast(image).enhance(2)

        # OCR
        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        return {
            "text": text.strip(),
            "confidence": 80
        }

    except Exception as e:
        return {
            "text": "",
            "confidence": 0,
            "error": str(e)
        }
