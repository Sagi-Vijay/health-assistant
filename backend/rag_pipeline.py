import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Global variable to hold the vector store
vector_store = None

def initialize_rag_pipeline(file_path: str):
    global vector_store
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")

    # 1. Load Data
    loader = TextLoader(file_path)
    documents = loader.load()

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    texts = text_splitter.split_documents(documents)

    # 3. Create Embeddings (using local model to save API calls)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Create Vector Store
    vector_store = FAISS.from_documents(texts, embeddings)
    
    print("RAG Pipeline Initialized and Index Built.")

def get_retriever():
    global vector_store
    if vector_store is None:
        raise ValueError("Vector store not initialized. Call initialize_rag_pipeline first.")
    
    return vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})
