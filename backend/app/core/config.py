from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_BASE_DIR = BASE_DIR / "uploads"
DOCUMENT_UPLOAD_DIR = UPLOAD_BASE_DIR / "documents"

DOCUMENT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
