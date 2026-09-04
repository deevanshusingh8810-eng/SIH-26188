def validate_document(ocr_result):

    text = ocr_result.get("text", "").strip()

    issues = []

    # Check whether OCR extracted any text
    if not text:
        issues.append("No readable text detected")

    # Check minimum text length
    if len(text) < 20:
        issues.append("Document contains insufficient readable text")

    # Check OCR errors
    if ocr_result.get("error"):
        issues.append("OCR processing failed")

    # Document is valid when no issues are found
    valid = len(issues) == 0

    return {
        "valid": valid,
        "issues": issues
    }
