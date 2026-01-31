from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import settings
from typing import List


class SplititerServiceError(Exception):
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
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
