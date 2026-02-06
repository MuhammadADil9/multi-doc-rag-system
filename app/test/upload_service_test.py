from app.services.upload_service import UploadService
from app.database.connection import SessionLocal
from app.models import Document, Chunk
import os


def test_upload_service():
    """Test the complete upload pipeline"""

    # Setup
    pdf_path = "app/battle_of_hattin.pdf"
    filename = "battle_of_hattin.pdf"

    db = SessionLocal()
    upload_service = UploadService()

    try:
        print("=" * 60)
        print("TESTING UPLOAD SERVICE")
        print("=" * 60)

        # Execute upload
        result = upload_service.process_upload(
            filepath=pdf_path,
            filename=filename,
            db=db,
        )

        print("\n" + "=" * 60)
        print("UPLOAD RESULT:")
        print("=" * 60)
        print(f"Document ID: {result['document_id']}")
        print(f"Filename: {result['filename']}")
        print(f"Total Chunks: {result['total_chunks']}")
        print(f"Message: {result['message']}")

        # Verify in database
        print("\n" + "=" * 60)
        print("VERIFYING DATABASE:")
        print("=" * 60)

        document = (
            db.query(Document).filter(Document.id == result["document_id"]).first()
        )

        if document:
            print(f"✓ Document found in DB")
            print(f"  - Filename: {document.file_name}")
            print(f"  - Total chunks: {document.total_chunks}")

            chunks = db.query(Chunk).filter(Chunk.document_id == document.id).all()

            print(f"✓ Found {len(chunks)} chunks in DB")
            print(f"  - First chunk preview: {chunks[0].chunk_text[:100]}...")
        else:
            print("✗ Document not found in DB")

        # Verify in Pinecone
        print("\n" + "=" * 60)
        print("VERIFYING PINECONE:")
        print("=" * 60)

        from app.services.vector_store import VectorStore
        from app.services.embeddings import EmbeddingsService

        vector_store = VectorStore()
        embedding_service = EmbeddingsService()

        # Search with first chunk as query
        query_embedding = embedding_service.generate_embeddings(
            chunks[0].chunk_text[:200]
        )
        search_results = vector_store.query(
            vector=query_embedding,
            top_k=3,
            metadata_filter={"document_id": str(document.id)},
        )

        print(f"✓ Found {len(search_results['matches'])} vectors in Pinecone")
        print(f"  - Top match score: {search_results['matches'][0]['score']:.4f}")
        print(f"  - Top match metadata: {search_results['matches'][0]['metadata']}")

        print("\n" + "=" * 60)
        print("✓ ALL VERIFICATIONS PASSED")
        print("=" * 60)

        # Cleanup
        print("\nCleaning up test data...")
        db.query(Chunk).filter(Chunk.document_id == document.id).delete()
        db.query(Document).filter(Document.id == document.id).delete()
        db.commit()
        print("✓ Cleanup complete")

    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_upload_service()
