from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    """Request body for query endpoint"""
    question: str
    documents_ids : List[str]
    top_k : int = 3

    class Config:
        json_schema_extra = {
            "example" : {
                "question" : "What happened in battle of Hattin in in 1187 ?",
                "documents_ids" : ["b55d58df-144d-4c86-a74c-011c1ec5b985"],
                "top_k" : 3
            }
        }


class SourceChunk(BaseModel):
    """Source chunk information"""
    chunk_id : str
    chunk_text : str
    chunk_index : int
    document_id : str
    score : float


class QueryResponse(BaseModel):
    """Data model for query endpoint response"""
    answer : str
    sources : List[SourceChunk]
    chat_id : str


