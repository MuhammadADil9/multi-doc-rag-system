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
    print("=" * 50)

    pc = Pinecone(
        api_key="pcsk_2NiKkS_TmjUzppAk6wDdD394WGhiks6dKzL8Wv35TDrGwyuLs7KuAKRnpsSK4oqLSV6zeF"
    )

    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            vector_type="dense",
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )


if __name__ == "__main__":
    try:
        create_index()
    except Exception as e:
        print(f"Error creating index: {e}")
        sys.exit(1)
