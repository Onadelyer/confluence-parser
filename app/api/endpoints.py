from fastapi import APIRouter, HTTPException, Depends
from app.schemas.models import QueryRequest, QueryResponse, GenerateRequest
from app.services.rag_service import RagService
from app.services.llm_factory import LLMFactory
from langchain_core.messages import HumanMessage

router = APIRouter()

def get_rag_service():
    return RagService()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest, service: RagService = Depends(get_rag_service)):
    return service.query(request.question)

@router.post("/generate")
async def generate_endpoint(request: GenerateRequest):
    try:
        llm = LLMFactory.create_chat_model()
        response = llm.invoke([HumanMessage(content=request.message)])
        return {
            "model": llm.model,
            "message": {
                "role": "assistant",
                "content": response.content
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
