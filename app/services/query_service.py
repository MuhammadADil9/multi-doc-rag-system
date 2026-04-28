from app.services.embeddings import EmbeddingsService
from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService
from app.models import Chunk, Chat
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime


class QueryServiceError(Exception):
    """Query service error"""
    pass


class QueryService:
    """Orchestrates the complete query pipeline"""
    
    def __init__(self):
        """Initialize all required services"""
        # TODO: Initialize services
        self.embedding_service = EmbeddingsService()
        self.vector_store = VectorStore()
        self.llm_service = LLMService()

    def process_query(
        self,
        question: str,
        document_ids: List[str],
        db: Session,
        top_k: int = 3,
        user_id: Optional[str] = None  # For Day 6
    ) -> Dict[str, Any]:
        """
        Complete query pipeline: question -> embedding -> pinecone search -> LLM -> answer.
        
        Args:
            question: User's question
            document_ids: List of document UUIDs to search within
            db: Database session
            top_k: Number of chunks to retrieve
            user_id: User ID (optional for now)
            
        Returns:
            {
                "answer": "Generated answer text",
                "sources": [
                    {
                        "chunk_id": "uuid",
                        "chunk_text": "...",
                        "chunk_index": 0,
                        "document_id": "uuid",
                        "score": 0.95
                    },
                    ...
                ],
                "chat_id": "uuid"
            }
        """
        
        try:
            print(f"\n{'='*60}")
            print(f"QUERY PIPELINE: {question[:50]}...")
            print(f"{'='*60}")
        
            print("\n[1/5] Embedding question...")
            question_embedding = self.embedding_service.generate_embeddings(question)
            print("Question embedding generated.")
            
            print("\n[2/5] Searching vector store...")
            # Build metadata filter for document_ids
            if len(document_ids) == 1:
                # Single document filter
                metadata_filter = {"document_id": document_ids[0]}
            else:
                # Multiple document filter
                metadata_filter = {"document_id": {"$in": document_ids}}

            results = self.vector_store.query(vector=question_embedding,top_k=top_k, metadata_filter=metadata_filter)  
            
            print(f"✓ Found {len(results['matches'])} matching chunks")
            
            print("\n[3/5] Fetching chunk details from database...")
            
            chunk_ids = [match['metadata']['chunk_id'] for match in results['matches']]
            
            chunks = db.query(Chunk).filter(Chunk.id.in_(chunk_ids)).all()
            
            chunk_map = {str(chunk.id): chunk for chunk in chunks}
            
            context_texts = []
            sources = []
            for match in results['matches']:
                chunk_id = match['metadata']['chunk_id']
                chunk = chunk_map.get(chunk_id)
                if chunk:
                    context_texts.append(chunk.chunk_text)
                    sources.append({
                        "chunk_id": chunk_id,
                        "chunk_text": chunk.chunk_text,
                        "chunk_index": chunk.chunk_index,
                        "document_id": str(chunk.document_id),
                        "score": match['score']
                    })
            print(f"✓ Retrieved chunk details for {len(context_texts)} chunks")
            
            print("\n[4/5] Generating answer with LLM...")
            answer = self.llm_service.generate_answer(question, context_texts)
            print("Answer generated.")
            
            print("\n[5/5] Saving chat to database...")
            
            chat = Chat(
                id=uuid.uuid4(),
                user_id=user_id,
                query=question,
                response=answer,
                document_ids=document_ids,
                created_at=datetime.utcnow()
            )
            
            db.add(chat)
            db.commit()
            db.refresh(chat)
            
            print(f"✓ Chat saved: {chat.id}")
            
            print(f"\n{'='*60}")
            print("✓ QUERY COMPLETE")
            print(f"{'='*60}\n")
            
            return {
                "answer": answer,
                "sources": sources,
                "chat_id": str(chat.id)
            }
            
        except Exception as e:
            db.rollback()
            raise QueryServiceError(f"Query failed: {e}") from e


