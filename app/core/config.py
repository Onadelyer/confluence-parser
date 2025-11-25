from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Ollama Config
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "gpt-oss:120b"
    OLLAMA_API_KEY: Optional[str] = None
    
    # Cloud/Chat Specific Config
    OLLAMA_CHAT_BASE_URL: Optional[str] = None
    OLLAMA_CHAT_MODEL: Optional[str] = None
    OLLAMA_CHAT_API_KEY: Optional[str] = None

    # Embedding Config
    OLLAMA_EMBEDDING_BASE_URL: Optional[str] = None
    OLLAMA_EMBEDDING_MODEL: Optional[str] = None
    OLLAMA_EMBEDDING_API_KEY: Optional[str] = None

    # Google Gemini Config
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_EMBEDDING_MODEL: str = "models/text-embedding-004"

    # Postgres Config
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    COLLECTION_NAME: str = "confluence_docs"

    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def chat_base_url(self) -> str:
        url = self.OLLAMA_CHAT_BASE_URL or self.OLLAMA_BASE_URL
        return self._clean_url(url)

    @property
    def chat_model(self) -> str:
        return self.OLLAMA_CHAT_MODEL or self.OLLAMA_MODEL

    @property
    def chat_api_key(self) -> Optional[str]:
        return self.OLLAMA_CHAT_API_KEY or self.OLLAMA_API_KEY

    @property
    def embedding_base_url(self) -> str:
        url = self.OLLAMA_EMBEDDING_BASE_URL or self.OLLAMA_BASE_URL
        return self._clean_url(url)
    
    @property
    def embedding_model_ollama(self) -> str:
        return self.OLLAMA_EMBEDDING_MODEL or self.OLLAMA_MODEL

    @property
    def embedding_api_key_ollama(self) -> Optional[str]:
        return self.OLLAMA_EMBEDDING_API_KEY or self.OLLAMA_API_KEY

    def _clean_url(self, url: str) -> str:
        if not url:
            return url
        if url.endswith("/api/chat"):
            return url.replace("/api/chat", "")
        elif url.endswith("/"):
            return url.rstrip("/")
        return url

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
