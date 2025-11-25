try:
    from langchain.chains import RetrievalQA
    print("Import successful: from langchain.chains import RetrievalQA")
except ImportError as e:
    print(f"Import failed: {e}")

try:
    from langchain.chains.retrieval_qa.base import RetrievalQA
    print("Import successful: from langchain.chains.retrieval_qa.base import RetrievalQA")
except ImportError as e:
    print(f"Import failed: {e}")

import langchain
print(f"Langchain version: {langchain.__version__}")
print(f"Langchain file: {langchain.__file__}")
