from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.services.llm_factory import LLMFactory
from app.services.vector_store import VectorStoreService
import logging

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self):
        self.llm = LLMFactory.create_chat_model()
        self.vector_store_service = VectorStoreService()

    def query(self, question: str):
        logger.info(f"Received query: {question}")
        
        try:
            retriever = self.vector_store_service.get_retriever()
            
            logger.info("Retrieving documents...")
            docs = retriever.invoke(question)
            logger.info(f"Retrieved {len(docs)} documents")
            for i, doc in enumerate(docs):
                logger.info(f"Doc {i}: {doc.metadata.get('title', 'No Title')} - {doc.page_content[:100]}...")
            
            context = "\n\n".join([doc.page_content for doc in docs])
            sources = list(set([doc.metadata.get("title", "Unknown") for doc in docs]))
            logger.info(f"Sources found: {sources}")
            
            template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
            prompt = ChatPromptTemplate.from_template(template)
            
            chain = (
                {"context": lambda x: context, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            logger.info("Invoking LLM chain...")
            answer = chain.invoke(question)
            logger.info("LLM response received")
            
            return {"answer": answer, "sources": sources}
            
        except Exception as e:
            logger.error(f"Error during query execution: {str(e)}", exc_info=True)
            return {"answer": f"Error during query: {str(e)}", "sources": []}
