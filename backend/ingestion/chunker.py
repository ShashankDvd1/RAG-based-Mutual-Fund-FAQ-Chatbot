from langchain_text_splitters import RecursiveCharacterTextSplitter

class Chunker:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def chunk_documents(self, parsed_docs):
        """
        Split parsed documents into overlapping text chunks.
        """
        chunks = []
        for doc in parsed_docs:
            text = doc["text"]
            metadata = doc["metadata"]
            
            # Split text using LangChain text splitter
            split_texts = self.text_splitter.split_text(text)
            
            total_chunks = len(split_texts)
            for idx, split_text in enumerate(split_texts):
                # Attach unique chunk ID and indices to metadata
                chunk_meta = metadata.copy()
                chunk_meta["chunk_index"] = idx
                chunk_meta["total_chunks"] = total_chunks
                chunk_meta["chunk_id"] = f"{metadata['filename'].replace('.', '_')}_chunk_{idx:03d}"
                
                chunks.append({
                    "text": split_text,
                    "metadata": chunk_meta
                })
                
        print(f"Split {len(parsed_docs)} documents into {len(chunks)} chunks.")
        return chunks

if __name__ == "__main__":
    chunker = Chunker()
    print("Chunker initialized.")
