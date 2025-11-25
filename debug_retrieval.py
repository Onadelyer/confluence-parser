import logging
from app.services.vector_store import VectorStoreService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_retrieve_all(limit: int = 20):
    """
    Retrieves a list of documents from the vector store for debugging.
    Since vector stores are designed for similarity search, we simulate "get all"
    by searching for a very generic term with a high limit.
    """
    logger.info(f"Attempting to retrieve up to {limit} documents for debugging...")
    
    service = VectorStoreService()
    vectorstore = service.get_vectorstore()
    
    # Use a generic query that is likely to match most text
    # Note: PGVector doesn't have a direct "list all" method exposed in this version of LangChain easily
    # so we use a similarity search with a high K.
    # Alternatively, we could use the underlying driver, but this tests the LangChain integration too.
    docs = vectorstore.similarity_search("the", k=limit)
    
    logger.info(f"Found {len(docs)} documents.")
    
    for i, doc in enumerate(docs):
        print(f"\n--- Document {i+1} ---")
        print(f"Source: {doc.metadata.get('title', 'Unknown')}")
        print(f"Content Snippet: {doc.page_content[:200]}...")
        print("-" * 20)

if __name__ == "__main__":
    debug_retrieve_all(limit=10)
