from app.services.pdf_parser import PDFParser
from app.services.text_splitter import TextSplitterService
from app.services.embeddings import EmbeddingsService
from app.services.vector_store import VectorStore
from app.models import Document, Chunk
from datetime import datetime
from app.config import settings
from sqlalchemy.orm import Session
import uuid
from typing import Dict, Any
from pathlib import Path


class UploadServiceError(Exception):
    """Upload service error"""

    pass


class UploadService:
    def __init__(self):
        self.pdf_parser = PDFParser()
        self.text_splitter = TextSplitterService()
        self.embeddings = EmbeddingsService()
        self.vector_store = VectorStore()

    def process_upload(
        self,
        filepath: str,
        filename: str,
        db: Session,
        user_id: str = None,
    ) -> Dict[str, Any]:
        """
        Complete upload pipeline with transaction management.
        """

        try:
            print(f"\n{'='*60}")
            print(f"UPLOAD PIPELINE: {filename}")
            print(f"{'='*60}")

            file_size_mb = Path(filepath).stat().st_size / (1024 * 1024)

            # STEP 1: Validate PDF
            print("\n[1/7] Validating PDF...")
            PDFParser.validate_file(
                pdf_file=filepath, max_size=settings.MAX_FILE_SIZE_MB
            )

            # STEP 2: Extract Text
            print("\n[2/7] Extracting text...")
            text = PDFParser.extract_text(pdf_path=filepath)

            # STEP 3: Split into Chunks
            print("\n[3/7] Splitting text...")
            chunks = self.text_splitter.split_text(text)

            # STEP 4: Generate Embeddings
            print("\n[4/7] Generating embeddings...")
            embeddings = self.embeddings.batch_embeddings(texts=chunks)

            # STEP 5: Create Document Record
            print("\n[5/7] Creating document record...")

            document_id = uuid.uuid4()

            document = Document(
                id=document_id,
                user_id=user_id,
                file_name=filename,
                file_size_mb=file_size_mb,
                upload_date=datetime.utcnow(),
                total_chunks=len(chunks),
            )

            db.add(document)
            db.flush()

            # STEP 6: Create Chunk Records
            print("\n[6/7] Creating chunk records...")

            chunk_records = []
            chunk_ids = []
            for idx, chunk_text in enumerate(chunks):
                chunk_id = uuid.uuid4()
                chunk_ids.append(str(chunk_id))

                chunk_records.append(
                    Chunk(
                        id=chunk_id,
                        document_id=document_id,
                        chunk_index=idx,
                        chunk_text=chunk_text,
                        created_at=datetime.utcnow(),
                    )
                )

            db.add_all(chunk_records)
            db.flush()

            # STEP 7: Upload to Pinecone
            print("\n[7/7] Uploading to Pinecone...")

            metadatas = [
                {
                    "chunk_id": chunk_id,
                    "document_id": str(document_id),
                    "chunk_index": idx,
                }
                for idx, chunk_id in enumerate(chunk_ids)
            ]

            self.vector_store.upsert(
                vectors=embeddings,
                ids=chunk_ids,
                metadata=metadatas,
            )

            # COMMIT TRANSACTION
            print("\n[COMMIT] All operations successful, committing...")
            db.commit()

            print(f"\n{'='*60}")
            print("✓ UPLOAD COMPLETE")
            print(f"{'='*60}\n")

            return {
                "document_id": str(document_id),
                "filename": filename,
                "total_chunks": len(chunks),
                "message": "Upload successful",
            }

        except Exception as e:
            db.rollback()
            raise UploadServiceError(f"Upload failed: {e}") from e
