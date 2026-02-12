from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.upload_service import UploadService, UploadServiceError
from app.config import settings
from typing import Dict, Any
from pathlib import Path
import shutil
import uuid

router = APIRouter(prefix="/document", tags=["document"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...), db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Upload and process a PDF document.
    """
    temp_file_path = None

    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400, detail=f"File {file.filename} is not a PDF."
            )

        temp_filename = f"{uuid.uuid4()}_{file.filename}"
        temp_file_path = UPLOAD_DIR / temp_filename

        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_size_mb = temp_file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds {settings.MAX_FILE_SIZE} limit.",
            )

        upload_service = UploadService()
        result = upload_service.process_upload(
            str(temp_file_path), filename=file.filename, db=db
        )
        if temp_file_path and temp_file_path.exists():
            temp_file_path.unlink()

        return result

    except UploadServiceError as e:
        if temp_file_path and temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

    except HTTPException:
        if temp_file_path and temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        if temp_file_path and temp_file_path.exists():
            temp_file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
