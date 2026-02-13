import uuid
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE_MB = 10


async def validate_pdf(file: UploadFile) -> bytes:
    """
    Validate uploaded PDF file:
    - Must be a .pdf file
    - Must start with %PDF (real PDF check)
    - Must be <= 10MB
    """

    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Read file contents
    contents = await file.read()

    # File size validation
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail="Maximum file size allowed is 10MB",
        )

    # Extension validation
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    # PDF magic bytes validation
    if not contents.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF file",
        )

    # Reset file pointer (important for further reads)
    await file.seek(0)

    return contents


def generate_secure_filename(original_name: str) -> str:
    """
    Generate a secure random filename while keeping .pdf extension
    """
    ext = original_name.split(".")[-1].lower()
    return f"{uuid.uuid4()}.{ext}"
