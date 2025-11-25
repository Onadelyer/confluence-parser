from langchain_ollama import ChatOllama
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMFactory:
    @staticmethod
    def create_chat_model():
        headers = {}
        if settings.chat_api_key:
            headers["Authorization"] = f"Bearer {settings.chat_api_key}"
        
        logger.info(f"Initializing ChatOllama with model: {settings.chat_model} at {settings.chat_base_url}")
        return ChatOllama(
            base_url=settings.chat_base_url,
            model=settings.chat_model,
            temperature=0,
            client_kwargs={"headers": headers} if headers else {}
        )

    @staticmethod
    def create_embeddings():
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        return GoogleGenerativeAIEmbeddings(
            model=settings.GOOGLE_EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY
        )
