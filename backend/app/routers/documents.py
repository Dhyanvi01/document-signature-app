from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.document import Document
from app.dependencies.auth import get_current_user   
from app.utils.file_utils import validate_pdf, generate_secure_filename
from app.core.config import DOCUMENT_UPLOAD_DIR

router = APIRouter(tags=["Documents"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    contents = await validate_pdf(file)

    stored_filename = generate_secure_filename(file.filename)
    file_path = DOCUMENT_UPLOAD_DIR / stored_filename

    with open(file_path, "wb") as f:
        f.write(contents)

    document = Document(
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_path=str(file_path),
        file_size=len(contents),
        content_type=file.content_type,
        owner_id=current_user.get("id") if isinstance(current_user, dict) else None,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return {
        "message": "PDF uploaded successfully",
        "document_id": document.id,
        "filename": document.original_filename,
    }
