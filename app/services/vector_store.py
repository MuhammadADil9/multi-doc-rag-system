from pinecone.grpc import PineconeGRPC as Pinecone
from app.config import settings
from typing import List


class PineconeError(Exception):
    pass


class VectorStore:
    """Vector Database Operation Management"""

    def __init__(self, index_name: str = "multi-doc-rag"):
        """Initialize pinecone connection"""
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(index_name)
        print("Pinecone connection established\n")

    def upsert(self, vectors: List[List[float]], ids: List[str], metadata: List[dict]):
        """Validate input lengths and upsert vectors into Pinecone"""
        if not (len(vectors) == len(ids) == len(metadata)):
            raise PineconeError("Vectors, ids, and metadata must have the same length")

        data = list(zip(ids, vectors, metadata))
        self.index.upsert(data)
        print(f"{len(vectors)} vectors upserted successfully")

    def query(self, vector: List[float], top_k: int = 5, metadata_filter: dict = None):
        """Query for similar vectors"""
        try:
            return self.index.query(
                vector=vector,
                top_k=top_k,
                filter=metadata_filter,
                include_metadata=True,
            )
        except PineconeError:
            raise PineconeError(f"Error querying vectors")
