import sqlite3
import json
from datetime import datetime
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "verification.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the required database tables if they don't exist."""

    connection = get_connection()
    cursor = connection.cursor()

    # Main document verification table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            file_type TEXT,
            ocr_data TEXT,
            validation_result TEXT,
            tampering_result TEXT,
            face_verification_result TEXT,
            risk_score REAL,
            overall_status TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    # Verification history / audit table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT NOT NULL,
            stage TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (document_id) REFERENCES documents(document_id)
        )
    """)

    connection.commit()
    connection.close()


def create_document(document_id, filename, file_type=None):
    """Create a new document record."""

    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO documents (
            document_id,
            filename,
            file_type,
            overall_status,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        document_id,
        filename,
        file_type,
        "uploaded",
        timestamp
    ))

    connection.commit()
    connection.close()


def add_history(document_id, stage, status):
    """Add an event to the verification history."""

    connection = get_connection()
    cursor = connection.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO verification_history (
            document_id,
            stage,
            status,
            timestamp
        )
        VALUES (?, ?, ?, ?)
    """, (
        document_id,
        stage,
        status,
        timestamp
    ))

    connection.commit()
    connection.close()


def update_document_result(
    document_id,
    ocr_data=None,
    validation_result=None,
    tampering_result=None,
    face_verification_result=None,
    risk_score=None,
    overall_status=None
):
    """Update verification results for an existing document."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE documents
        SET
            ocr_data = COALESCE(?, ocr_data),
            validation_result = COALESCE(?, validation_result),
            tampering_result = COALESCE(?, tampering_result),
            face_verification_result = COALESCE(?, face_verification_result),
            risk_score = COALESCE(?, risk_score),
            overall_status = COALESCE(?, overall_status)
        WHERE document_id = ?
    """, (
        json.dumps(ocr_data) if ocr_data is not None else None,
        json.dumps(validation_result) if validation_result is not None else None,
        json.dumps(tampering_result) if tampering_result is not None else None,
        json.dumps(face_verification_result) if face_verification_result is not None else None,
        risk_score,
        overall_status,
        document_id
    ))

    connection.commit()
    connection.close()


def get_document(document_id):
    """Get the complete verification result for a document."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM documents
        WHERE document_id = ?
    """, (document_id,))

    document = cursor.fetchone()

    connection.close()

    if document is None:
        return None

    result = dict(document)

    # Convert stored JSON strings back into Python objects
    for field in [
        "ocr_data",
        "validation_result",
        "tampering_result",
        "face_verification_result"
    ]:
        if result[field]:
            result[field] = json.loads(result[field])

    return result


def get_history(document_id):
    """Get verification history for a document."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            document_id,
            stage,
            status,
            timestamp
        FROM verification_history
        WHERE document_id = ?
        ORDER BY id ASC
    """, (document_id,))

    history = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return history


# Initialize the database when this module is imported.
initialize_database()