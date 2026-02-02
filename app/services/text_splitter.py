from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings
from typing import List


class TextSplitterError(Exception):
    pass


class TextSplitterService:
    """
    split text into chunks
    """

    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        chunk_overlap: int = settings.CHUNK_OVERLAP,
    ):
        """Initialize RecursiveCharacterTextSplitter with parameter"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def split_text(self, text: str) -> List[str]:
        """Break down strign into chunks"""

        return self.text_splitter.split_text(text)
