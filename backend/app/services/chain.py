from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from typing import List
from datetime import datetime
from langchain_core.documents import Document

class RAGChain:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a facts-only mutual fund FAQ assistant. 
Use ONLY the provided context to answer the question. Do not make assumptions or extrapolate.
If the answer is not contained in the provided context, state: "I cannot find the answer in the provided documents."

Rules:
1. Answer in 3 sentences or fewer. Keep it concise.
2. Include the source link (exactly as given in the context metadata) in your response as a markdown link, e.g. [Official Scheme Details](URL).
3. End your response with a line in this format: "Last updated from sources: [Date]" where [Date] is the access date from the context metadata.
"""),
            ("human", "Context:\n{context}\n\nQuestion: {question}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()

    def generate(self, question: str, context_docs: List[Document]) -> str:
        """
        Format retrieved documents, invoke the RAG chain, and return the response.
        """
        if not context_docs:
            return "I cannot find any relevant documents in the database to answer this question."

        context_str = ""
        for i, doc in enumerate(context_docs):
            source_url = doc.metadata.get("source_url", "https://www.sbimf.com")
            date_accessed = doc.metadata.get("date_accessed", datetime.now().strftime("%B %d, %Y"))
            context_str += f"[Document {i+1}]\nMetadata: Source URL={source_url}, Access Date={date_accessed}\nContent: {doc.page_content}\n\n"

        response = self.chain.invoke({
            "context": context_str,
            "question": question
        })
        
        return response

# Singleton instance
chain_instance = None

def get_rag_chain():
    global chain_instance
    if chain_instance is None:
        chain_instance = RAGChain()
    return chain_instance
