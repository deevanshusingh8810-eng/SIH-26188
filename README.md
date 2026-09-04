SIH26188 — AI-Based Fake Identity & Document Screening System

Project Overview

This project is a backend prototype for the SIH Problem Statement 26188: AI-Based Fake Identity & Document Screening System.

The system allows a document to be uploaded and processed through a verification pipeline consisting of:

- Document upload and storage
- OCR text extraction
- Document validation
- Tampering detection
- Face detection
- Risk score calculation
- Final document risk classification

Student 1 Backend Workflow

Upload Document
      ↓
Generate Document ID
      ↓
Store Document
      ↓
Document Lookup
      ↓
OCR
      ↓
Validation
      ↓
Tampering Detection
      ↓
Face Verification
      ↓
Risk Engine
      ↓
Final Risk Status

Project Structure

SIH-26188/
│
├── ai/
│   ├── __init__.py
│   ├── ocr.py
│   ├── validation.py
│   ├── tampering.py
│   ├── face_verification.py
│   └── risk_engine.py
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── uploads/
│
├── requirements.txt
└── README.md

Installation

Clone or copy the project and move into the project directory:

cd SIH-26188

Create a virtual environment:

python3 -m venv venv

Activate the virtual environment:

source venv/bin/activate

Install Python dependencies:

pip install -r requirements.txt

Tesseract OCR Installation

The OCR module requires Tesseract OCR to be installed on the system.

For Ubuntu/Linux Mint:

sudo apt update
sudo apt install tesseract-ocr

Check installation:

tesseract --version

Running the Backend

Activate the virtual environment:

source venv/bin/activate

Start the FastAPI server:

uvicorn backend.main:app --reload

The backend will run at:

http://127.0.0.1:8000

Swagger API documentation is available at:

http://127.0.0.1:8000/docs

API Endpoints

GET /

Checks whether the backend is running.

Example response:

{
  "message": "SIH 26188 Backend is working!"
}

GET /health

Checks backend health.

Example response:

{
  "status": "healthy"
}

POST /upload

Uploads a document.

Supported file types:

- JPG
- JPEG
- PNG
- PDF

Example response:

{
  "message": "Document uploaded successfully",
  "document_id": "generated-uuid",
  "filename": "document.png",
  "saved_as": "generated-uuid.png"
}

GET /document/{document_id}

Checks whether an uploaded document exists.

Example response:

{
  "document_id": "generated-uuid",
  "filename": "generated-uuid.png",
  "file_type": ".png",
  "status": "found"
}

POST /ocr/{document_id}

Runs OCR on an uploaded document.

POST /analyze/{document_id}

Runs the complete verification pipeline:

- OCR
- Validation
- Tampering detection
- Face detection
- Risk score calculation

Example response structure:

{
  "success": true,
  "document_id": "generated-uuid",
  "filename": "generated-uuid.png",
  "analysis": {
    "risk_score": 0,
    "final_status": "low_risk",
    "reasons": []
  },
  "results": {
    "ocr": {},
    "validation": {},
    "tampering": {},
    "face_verification": {}
  }
}

Current Status

Student 1 — Backend Integration

Completed:

- FastAPI backend setup
- Document upload API
- File type validation
- UUID document ID generation
- File storage
- Document lookup API
- OCR endpoint
- Complete analysis endpoint
- OCR integration
- Validation integration
- Tampering detection integration
- Face detection integration
- Risk engine integration
- Standardized API response
- End-to-end backend testing

Future Integration

The backend is designed to integrate with:

- Advanced structured OCR extraction
- Improved document validation
- Advanced AI tampering detection
- Face-to-face identity comparison
- Database storage
- Verification history
- Frontend dashboard
- Final team integration
