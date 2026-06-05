import os
from langchain_community.vectorstores import FAISS
from app.core.embeddings import get_embeddings
from app.core.config import settings

class FAISSRetriever:
    def __init__(self):
        self.embeddings = get_embeddings()
        self.vectorstore_path = settings.VECTORSTORE_PATH
        if not os.path.isabs(self.vectorstore_path):
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.vectorstore_path = os.path.normpath(os.path.join(backend_dir, self.vectorstore_path))
            
        print(f"Loading FAISS index from: {self.vectorstore_path}")
        if not os.path.exists(self.vectorstore_path):
            raise FileNotFoundError(f"FAISS vector store not found at {self.vectorstore_path}. Run ingestion first.")
            
        self.db = FAISS.load_local(
            self.vectorstore_path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query: str, scheme_name: str = None, k: int = 4):
        """
        Perform similarity search and filter results by scheme_name if specified.
        If a scheme is chosen, returns documents matching that scheme or 'General'.
        """
        # If scheme_name is provided, query more docs to guarantee we hit enough matching chunks after filtering
        search_k = k * 4 if scheme_name and scheme_name != "General" else k
        docs = self.db.similarity_search(query, k=search_k)

        if not scheme_name or scheme_name == "General":
            return docs[:k]

        # Filter: match exact scheme or General documents (like statement/FAQ guides)
        filtered_docs = []
        for doc in docs:
            doc_scheme = doc.metadata.get("scheme_name")
            if doc_scheme == scheme_name or doc_scheme == "General":
                filtered_docs.append(doc)
                if len(filtered_docs) >= k:
                    break
        
        # If no documents matched the filter, fallback to returning the top standard search results
        if not filtered_docs:
            print(f"WARNING: No chunks matched scheme filter '{scheme_name}'. Falling back to unfiltered results.")
            return docs[:k]

        return filtered_docs

# Singleton instance
retriever_instance = None

def get_retriever():
    global retriever_instance
    if retriever_instance is None:
        retriever_instance = FAISSRetriever()
    return retriever_instance
