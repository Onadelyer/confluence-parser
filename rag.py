# import os
# from langchain_ollama import OllamaEmbeddings, ChatOllama
# from langchain_community.vectorstores import Chroma
# from langchain.chains import RetrievalQA
# from dotenv import load_dotenv

# load_dotenv()

# OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# PERSIST_DIRECTORY = "./chroma_db"

# def get_vectorstore():
#     embeddings = OllamaEmbeddings(
#         base_url=OLLAMA_BASE_URL,
#         model=OLLAMA_MODEL
#     )
#     if os.path.exists(PERSIST_DIRECTORY):
#         return Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
#     return None

# def query_rag(question: str):
#     vectorstore = get_vectorstore()
#     if not vectorstore:
#         return {"answer": "Knowledge base is empty. Please ingest documents first.", "sources": []}
    
#     llm = ChatOllama(
#         base_url=OLLAMA_BASE_URL,
#         model=OLLAMA_MODEL,
#         temperature=0
#     )
    
#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
#         return_source_documents=True
#     )
    
#     result = qa_chain({"query": question})
    
#     answer = result["result"]
#     sources = list(set([doc.metadata.get("title", "Unknown") for doc in result["source_documents"]]))
    
#     return {"answer": answer, "sources": sources}
