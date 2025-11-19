from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from models import QueryRequest, QueryResponse, GenerateRequest
# from rag import query_rag, OLLAMA_BASE_URL, OLLAMA_MODEL
import os
from dotenv import load_dotenv
load_dotenv()  # load .env into environment

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
LLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
print(f"Using OLLAMA_MODEL: {LLAMA_API_KEY}")

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
    print(LLAMA_API_KEY)
    if not LLAMA_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OLLAMA_API_KEY")

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "user", "content": request.message}
        ],
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://ollama.com/api/chat",
                json=payload,
                headers=headers,
                timeout=90
            )
            resp.raise_for_status()
            return resp.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=e.response.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.responses import StreamingResponse

@app.post("/generate-stream")
async def generate_stream_endpoint(request: GenerateRequest):
    import httpx, os, json

    LLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY")
    if not LLAMA_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OLLAMA_API_KEY")

    headers = {
        "Authorization": f"Bearer {LLAMA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "user", "content": request.message}
        ],
        "stream": True
    }

    async def stream():
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "https://ollama.com/api/chat",
                json=payload,
                headers=headers,
                timeout=300
            ) as resp:
                resp.raise_for_status()

                async for line in resp.aiter_lines():
                    if line.strip():
                        # each `line` is a separate JSON object like:
                        # {"type":"response","message": {...}}
                        yield line + "\n"

    return StreamingResponse(stream(), media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
