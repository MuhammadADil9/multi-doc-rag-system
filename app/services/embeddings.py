from sentence_transformers import SentenceTransformer
from typing import List


class EmbeddingsError(Exception):
    """Embeddings error"""


class EmbeddingsService:
    """Load model and generate embeddings"""

    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        """load model"""
        self.model = SentenceTransformer(model_name)
        print(f"Model :- {model_name} loaded")

    def generate_embeddings(self, text: str) -> List[float]:
        """generate embeddings"""
        # all-mpnet-base-v2  returns a numpy array of embeddings.
        # convert it into list of float.

        try:
            if not text.strip():
                raise EmbeddingsError("Text is empty")

            return self.model.encode(text).tolist()

        except EmbeddingsError:
            raise EmbeddingsError("Error generating embeddings")

    def batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """generate batch embeddings"""
        try:
            if not texts or any(not text.strip() for text in texts):
                raise EmbeddingsError("Empty text found in batch")

            return self.model.encode(texts).tolist()

        except EmbeddingsError:
            raise EmbeddingsError("Error generating batch embeddings")
