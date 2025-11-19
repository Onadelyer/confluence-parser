from fastapi import FastAPI, HTTPException, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse, GenerateRequest
# from rag import query_rag, OLLAMA_BASE_URL, OLLAMA_MODEL
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

app = FastAPI(title="Confluence RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        result = query_rag(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint: forwards message to Ollama /api/generate
@app.post("/generate")
async def generate_endpoint(request: GenerateRequest):
    import httpx
    try:
        print(request.message)
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": request.message,
            "stream": False
        }
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=60)
            print(resp.status_code, resp.text)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import StreamingResponse

@app.post("/generate-stream")
async def generate_endpoint(request: GenerateRequest):
    import httpx

    async def stream():
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_BASE_URL}/api/generate",
                json={"model": OLLAMA_MODEL, "prompt": request.message},
                timeout=60
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line.strip():
                        yield line + "\n"

    return StreamingResponse(stream(), media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
