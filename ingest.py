import os
from langchain_community.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

PERSIST_DIRECTORY = "./chroma_db"

def ingest_docs():
    if not all([CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN]):
        raise ValueError("Confluence credentials not set")

    print(f"Connecting to Confluence at {CONFLUENCE_URL}...")
    loader = ConfluenceLoader(
        url=CONFLUENCE_URL,
        username=CONFLUENCE_USERNAME,
        api_key=CONFLUENCE_API_TOKEN
    )
    
    # Load all pages (limit can be adjusted)
    print("Loading documents...")
    documents = loader.load(limit=50) 
    print(f"Loaded {len(documents)} documents.")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")
    
    print(f"Creating embeddings using Ollama ({OLLAMA_MODEL})...")
    embeddings = OllamaEmbeddings(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL
    )
    
    # Create and persist vectorstore
    print("Creating vector store...")
    vectorstore = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings, 
        persist_directory=PERSIST_DIRECTORY
    )
    vectorstore.persist()
    print(f"Successfully ingested {len(documents)} documents into {PERSIST_DIRECTORY}")

if __name__ == "__main__":
    ingest_docs()
