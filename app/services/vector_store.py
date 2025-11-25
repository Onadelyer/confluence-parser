from langchain_postgres import PGVector
from app.core.config import settings
from app.services.llm_factory import LLMFactory
import logging

logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self):
        self.embeddings = LLMFactory.create_embeddings()
        self.connection_string = settings.database_url
        self.collection_name = settings.COLLECTION_NAME

    def get_vectorstore(self):
        try:
            vectorstore = PGVector(
                embeddings=self.embeddings,
                collection_name=self.collection_name,
                connection=self.connection_string,
                use_jsonb=True,
            )
            logger.info("Vectorstore connection established")
            return vectorstore
        except Exception as e:
            logger.error(f"Error connecting to vectorstore: {e}")
            raise e

    def get_retriever(self, k: int = 3):
        vectorstore = self.get_vectorstore()
        return vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
