from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

from ai.ocr import run_ocr
from ai.validation import validate_document
from ai.tampering import detect_tampering
from ai.face_verification import detect_face
from ai.risk_engine import calculate_risk
app = FastAPI(
    title="SIH 26188 Backend"
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "SIH 26188 Backend is working!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf"}

    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG and PDF files are allowed"
        )

    document_id = str(uuid.uuid4())

    new_filename = f"{document_id}{file_extension}"

    file_path = UPLOAD_DIR / new_filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Document uploaded successfully",
        "document_id": document_id,
        "filename": file.filename,
        "saved_as": new_filename
    }


@app.get("/document/{document_id}")
def get_document(document_id: str):

    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]

    for extension in allowed_extensions:
        file_path = UPLOAD_DIR / f"{document_id}{extension}"

        if file_path.exists():
            return {
                "document_id": document_id,
                "filename": file_path.name,
                "file_type": extension,
                "status": "found"
            }

    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )


@app.post("/analyze/{document_id}")
def analyze_document(document_id: str):

    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]

    file_path = None

    for extension in allowed_extensions:
        possible_path = UPLOAD_DIR / f"{document_id}{extension}"

        if possible_path.exists():
            file_path = possible_path
            break

    if file_path is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # OCR
    try:
        ocr_result = run_ocr(str(file_path))
    except Exception as e:
        ocr_result = {
            "error": str(e),
            "text": "",
            "confidence": 0
        }

    # Validation
    try:
        validation_result = validate_document(ocr_result)
    except Exception as e:
        validation_result = {
            "valid": False,
            "issues": [f"Validation error: {str(e)}"]
        }

    # Tampering detection
    try:
        tampering_result = detect_tampering(str(file_path))
    except Exception as e:
        tampering_result = {
            "tampering_score": 100,
            "suspicious": True,
            "details": [f"Tampering analysis error: {str(e)}"]
        }

    # Face detection
    try:
        face_result = detect_face(str(file_path))
    except Exception as e:
        face_result = {
            "face_detected": False,
            "face_count": 0,
            "error": str(e)
        }

    # Risk calculation
    try:
        risk_result = calculate_risk(
            validation_result,
            tampering_result,
            face_result
        )
    except Exception as e:
        risk_result = {
            "risk_score": 100,
            "final_status": "high_risk",
            "reasons": [f"Risk calculation error: {str(e)}"]
        }

    return {
        "success": True,
        "document_id": document_id,
        "filename": file_path.name,
        "analysis": risk_result,
        "results": {
            "ocr": ocr_result,
            "validation": validation_result,
            "tampering": tampering_result,
            "face_verification": face_result
        }
    }


@app.post("/ocr/{document_id}")
def ocr_document(document_id: str):

    allowed_extensions = [".jpg", ".jpeg", ".png", ".pdf"]

    file_path = None

    for extension in allowed_extensions:
        possible_path = UPLOAD_DIR / f"{document_id}{extension}"

        if possible_path.exists():
            file_path = possible_path
            break

    if file_path is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    ocr_result = run_ocr(str(file_path))

    return {
        "document_id": document_id,
        "filename": file_path.name,
        "ocr": ocr_result
    }
