def calculate_risk(validation_result, tampering_result, face_result):

    risk_score = 0
    reasons = []

    # Validation risk
    if not validation_result.get("valid", False):
        risk_score += 30
        reasons.append("Document validation failed")

    # Tampering risk
    tampering_score = tampering_result.get("tampering_score", 0)
    risk_score += tampering_score

    if tampering_result.get("suspicious", False):
        reasons.append("Possible document tampering detected")

    # Face-related check
    if not face_result.get("face_detected", False):
        risk_score += 10
        reasons.append("No face detected in document")

    # Limit score between 0 and 100
    risk_score = min(100, risk_score)

    # Final classification
    if risk_score >= 70:
        final_status = "high_risk"
    elif risk_score >= 40:
        final_status = "suspicious"
    else:
        final_status = "low_risk"

    return {
        "risk_score": risk_score,
        "final_status": final_status,
        "reasons": reasons
    }
