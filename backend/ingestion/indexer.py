import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

class Indexer:
    def __init__(self, embedding_model="BAAI/bge-small-en-v1.5"):
        print(f"Initializing local embedding model: {embedding_model} for ingestion...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={'device': 'cpu'}
        )

    def create_and_save_index(self, chunks, output_path="backend/data/vectorstore"):
        """
        Embed chunks and build the FAISS index, persisting it to output_path.
        """
        if not chunks:
            print("No chunks to index.")
            return False

        texts = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]

        print(f"Generating embeddings for {len(chunks)} chunks and building FAISS index...")
        
        # Build the FAISS vector store
        db = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )

        # Save the vector store local to the disk
        os.makedirs(output_path, exist_ok=True)
        print(f"Saving FAISS index to {output_path}...")
        db.save_local(output_path)
        print("Successfully created and saved FAISS index.")
        return True

if __name__ == "__main__":
    indexer = Indexer()
    print("Indexer initialized.")
