import os
import sys
from dotenv import load_dotenv

# Ensure we can import modules from parent directory if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parser import Parser
from chunker import Chunker
from indexer import Indexer

def main():
    print("=== Starting RAG Ingestion Pipeline ===")
    
    # 1. Load environment variables
    # Check if we are running from backend/ or root folder and locate .env
    env_loaded = load_dotenv()
    if not env_loaded:
        # Fallback to parent path
        load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))
    
    # Configure directories
    # Default paths relative to backend root
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(backend_dir, "data", "raw")
    vectorstore_path = os.getenv("VECTORSTORE_PATH", os.path.join(backend_dir, "data", "vectorstore"))
    embedding_model = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    print(f"Loading raw documents from: {raw_dir}")
    print(f"Target vector store path: {vectorstore_path}")
    print(f"Embedding model: {embedding_model}")

    # 2. Parse Documents
    parser = Parser(raw_dir=raw_dir)
    parsed_docs = parser.parse_all()
    if not parsed_docs:
        print("Error: No documents were parsed. Exiting ingestion.")
        sys.exit(1)

    # 3. Chunk Documents
    chunker = Chunker(chunk_size=500, chunk_overlap=100)
    chunks = chunker.chunk_documents(parsed_docs)
    if not chunks:
        print("Error: No text chunks generated. Exiting ingestion.")
        sys.exit(1)

    # 4. Index Chunks
    indexer = Indexer(embedding_model=embedding_model)
    success = indexer.create_and_save_index(chunks, output_path=vectorstore_path)

    if success:
        print("=== RAG Ingestion Pipeline Completed Successfully ===")
    else:
        print("=== RAG Ingestion Pipeline Failed ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
