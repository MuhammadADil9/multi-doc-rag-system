from app.services.pdf_parser import PDFParser
from app.services.text_splitter import TextSplitterService
from app.services.embeddings import EmbeddingsService
from app.services.vector_store import VectorStore
from app.config import settings
import uuid


def test_day_two_pipeline():
    """Test: PDF → Chunks → Embeddings → Pinecone"""

    print("=" * 60)
    print("DAY 3: EMBEDDING & VECTOR STORE PIPELINE TEST")
    print("=" * 60)

    # Parse PDF (reusing Day 1)
    pdf_path = "app/battle_of_hattin.pdf"
    print("\n[1/5] Parsing PDF...")
    text = PDFParser.extract_text(pdf_path)
    print(f"✓ Extracted {len(text)} characters")

    # Split into chunks
    print("\n[2/5] Splitting text...")
    splitter = TextSplitterService()
    chunks = splitter.split_text(text)
    print(f"✓ Created {len(chunks)} chunks")

    # Generate embeddings
    print("\n[3/5] Generating embeddings...")
    embedding_service = EmbeddingsService()
    embeddings = embedding_service.batch_embeddings(chunks)
    print(f"✓ Generated {len(embeddings)} embeddings")
    print(f"  - Embedding dimension: {len(embeddings[0])}")

    # Prepare metadata
    print("\n[4/5] Preparing Pinecone data...")
    document_id = str(uuid.uuid4())
    chunk_ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [
        {"document_id": document_id, "chunk_index": idx, "chunk_id": chunk_id}
        for idx, chunk_id in enumerate(chunk_ids)
    ]
    print(f"✓ Document ID: {document_id}")
    print(f"✓ Prepared {len(chunk_ids)} chunk IDs")

    # Upload to Pinecone
    print("\n[5/5] Uploading to Pinecone...")
    vector_store = VectorStore()
    vector_store.upsert(vectors=embeddings, ids=chunk_ids, metadata=metadatas)
    print("✓ Upload complete")

    print("\n" + "=" * 60)
    print("BONUS: Testing Vector Search")
    print("=" * 60)

    # Using beginning of chunks as query
    query_text = chunks[0][:100]
    print(f"Query text: '{query_text}...'")

    query_embedding = embedding_service.generate_embeddings(query_text)
    results = vector_store.query(vector=query_embedding, top_k=3)

    print(f"\n✓ Found {len(results['matches'])} matches:")
    for i, match in enumerate(results["matches"], 1):
        print(f"\n  Match {i}:")
        print(f"    - Score: {match['score']:.4f}")
        print(f"    - Chunk ID: {match['id']}")
        print(f"    - Metadata: {match['metadata']}")

    print("\n" + "=" * 60)
    print("✓ EMBEDDINGS & VECTOR STORE WORKING")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_day_two_pipeline()
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback

        traceback.print_exc()
