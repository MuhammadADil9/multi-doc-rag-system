from pinecone.grpc import PineconeGRPC as Pinecone
from app.config import settings
from typing import List
from pinecone import Vector


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
        try:
            """Validate input lengths and upsert vectors into Pinecone"""
            if not (len(vectors) == len(ids) == len(metadata)):
                raise PineconeError(
                    "Vectors, ids, and metadata must have the same length"
                )
            # Issue is that passed argument isn't the one which is expected as by the parameter.
            # Passing down values by wrapping it up in a special Vector data structure.
            data = [
                Vector(id=id_, values=vector, metadata=meta)
                for id_, vector, meta in zip(ids, vectors, metadata)
                ]
            self.index.upsert(data)

            print(f"{len(vectors)} vectors upserted successfully")
        except PineconeError:
            raise PineconeError(f"Error upserting vectors")

    def query(self, vector: List[float], top_k: int = 5, metadata_filter = None):
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
