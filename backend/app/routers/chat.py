from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from app.services.retriever import get_retriever
from app.services.chain import get_rag_chain
from app.services.guardrails import get_guardrails

router = APIRouter(prefix="/api")

class ChatRequest(BaseModel):
    question: str
    scheme: Optional[str] = None

class ChunkInfo(BaseModel):
    content: str
    source_url: str
    scheme_name: str
    document_type: str
    date_accessed: str
    title: str

class ChatResponse(BaseModel):
    answer: str
    retrieved_chunks: List[ChunkInfo]

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    question = request.question.strip()
    scheme = request.scheme.strip() if request.scheme else None
    
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    guardrails = get_guardrails()
    retriever = get_retriever()
    rag_chain = get_rag_chain()

    # 1. Run Pre-Retrieval Guardrails (PII and Advice Refusal)
    is_safe, refusal_msg = guardrails.check_pre_retrieval(question)
    if not is_safe:
        return ChatResponse(
            answer=refusal_msg,
            retrieved_chunks=[]
        )

    # 2. Retrieve relevant chunks (filtered by scheme if specified)
    try:
        docs = retriever.retrieve(query=question, scheme_name=scheme, k=3)
    except Exception as e:
        print(f"Error during retrieval: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve information from database: {str(e)}")

    # 3. Generate response using Groq RAG chain
    try:
        answer = rag_chain.generate(question=question, context_docs=docs)
    except Exception as e:
        print(f"Error during generation: {e}")
        raise HTTPException(status_code=500, detail="LLM generation error. Check your API key and limits.")

    # 4. Run Post-Generation Guardrails (Citation Enforcer)
    final_answer = guardrails.enforce_citations(answer, docs)

    # 5. Format retrieved chunks for response
    formatted_chunks = []
    for doc in docs:
        formatted_chunks.append(ChunkInfo(
            content=doc.page_content,
            source_url=doc.metadata.get("source_url", "https://www.sbimf.com"),
            scheme_name=doc.metadata.get("scheme_name", "General"),
            document_type=doc.metadata.get("document_type", "factsheet"),
            date_accessed=doc.metadata.get("date_accessed", "June 1, 2026"),
            title=doc.metadata.get("title", "SBI Factsheet")
        ))

    return ChatResponse(
        answer=final_answer,
        retrieved_chunks=formatted_chunks
    )
