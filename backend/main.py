from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid
from ai.ocr import run_ocr
from ai.validation import validate_document
from ai.tampering import detect_tampering


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

    ocr_result = run_ocr(str(file_path))

    validation_result = validate_document(ocr_result)

    tampering_result = detect_tampering(str(file_path))

    return {
        "document_id": document_id,
        "filename": file_path.name,
        "ocr": ocr_result,
        "validation": validation_result,
        "tampering": tampering_result
    }