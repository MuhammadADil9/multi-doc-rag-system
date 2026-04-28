from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.query_service import QueryService, QueryServiceError
from typing import List, Dict, Any
from app.schemas.query_schema import QueryRequest, QueryResponse


router = APIRouter(
    prefix="/query",
    tags=["query"]
)   


@router.post("/", response_model=QueryResponse)
async def query_documents(
    request:QueryRequest,
    db:Session = Depends(get_db),
) -> QueryResponse:
    """
    Ask a question about uploaded documents.

    Process 
    > Embed the question 
    > Search pinecone for relevant chunks 
    > fetch chunk text from postgreSQL
    > Generate answer using LLM 
    > Save chat to database 
    > Return answer with sources 


    Args:
        request: Query request with question and document IDs
        db: Database session
        
    Returns:
        Answer with source chunks and chat ID
    """

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(request.documents_ids) == 0:
        raise HTTPException(status_code=400, detail="Document Ids cannot be empty")

    if request.top_k < 1 or request.top_k > 10:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 10")
    
    try:                                          # ← ADD THIS
        query_service = QueryService()
        result = query_service.process_query(
            question=request.question,
            document_ids=request.documents_ids,
            db=db,
            top_k=request.top_k
        )
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            chat_id=result["chat_id"]
        )
    
    except HTTPException:                         # ← NOW REACHABLE
        raise
    
    except QueryServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))