from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from app.config import settings
import sys


def create_index():
    """create pinecone index"""

    index_name = "multi-doc-rag"
    DIMENSION = 768
    METRIC = "cosine"

    print("Creating pinecone index")

    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            vector_type="dense",
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_ENV),
        )

    print("\nIndex created successfully")


if __name__ == "__main__":
    try:
        create_index()
    except Exception as e:
        print(f"Error creating index: {e}")
        sys.exit(1)
