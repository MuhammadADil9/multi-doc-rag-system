from app.database.connection import SessionLocal
from app.models import Document, Chunk, Chat
import uuid
from datetime import datetime


def test_database_operations():
    db = SessionLocal()

    try:
        print("=" * 60)
        print("DAY 3: CRUD OPERATIONS ON DATABASE")
        print("=" * 60)

        # ==================== TEST 1: Create Document ====================
        print("\n[TEST 1] Creating Document...")

        document = Document(
            id=uuid.uuid4(),
            file_name="test_sample.pdf",
            file_size_mb=2.5,
            upload_date=datetime.utcnow(),
            total_chunks=10,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        print(f"✓ Document created: {document.id}")
        print(f"  file_name: {document.file_name}")

        # ==================== TEST 2: Create Chunks ====================
        print("\n[TEST 2] Creating Chunks...")

        chunks = [
            Chunk(
                id=uuid.uuid4(),
                document_id=document.id,
                chunk_index=i,
                chunk_text=f"This is chunk {i} content...",
                created_at=datetime.utcnow(),
            )
            for i in range(3)
        ]

        db.add_all(chunks)
        db.commit()

        print(f"✓ Created {len(chunks)} chunks")

        # ==================== TEST 3: Query Document with Chunks ====================
        print("\n[TEST 3] Querying Document with Chunks...")

        queried_doc = db.query(Document).filter(Document.id == document.id).first()

        print(f"✓ Found document: {queried_doc.file_name}")
        print(f"  Total chunks in DB: {len(queried_doc.chunks)}")

        # Print first chunk text
        print(f"  First chunk text: {queried_doc.chunks[0].chunk_text[:50]}...")

        # ==================== TEST 4: Query Chunks by Document ID ====================
        print("\n[TEST 4] Querying Chunks by Document ID...")

        doc_chunks = db.query(Chunk).filter(Chunk.document_id == document.id).all()

        print(f"✓ Found {len(doc_chunks)} chunks for document")
        for chunk in doc_chunks:
            print(f"  - Chunk {chunk.chunk_index}: {chunk.chunk_text[:50]}...")

        # ==================== TEST 5: Create Chat ====================
        print("\n[TEST 5] Creating Chat Record...")

        chat = Chat(
            id=uuid.uuid4(),
            query="What is this document about?",
            response="This document discusses...",
            document_ids=[document.id],  # Array of UUIDs
            created_at=datetime.utcnow(),
        )

        db.add(chat)
        db.commit()

        print(f"✓ Chat created: {chat.id}")
        print(f"  Query: {chat.query}")
        print(f"  Used {len(chat.document_ids)} document(s)")

        # ==================== TEST 6: Cleanup ====================
        print("\n[TEST 6] Cleaning up test data...")

        db.query(Chunk).filter(Chunk.document_id == document.id).delete()
        db.query(Document).filter(Document.id == document.id).delete()
        db.query(Chat).filter(Chat.id == chat.id).delete()
        db.commit()

        print("✓ Test data cleaned up")

        print("\n" + "=" * 60)
        print("✓ ALL DATABASE TESTS PASSED")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_database_operations()
