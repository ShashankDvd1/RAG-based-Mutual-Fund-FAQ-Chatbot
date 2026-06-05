import re
from typing import Optional, Tuple, List
from langchain_core.documents import Document

class GuardrailsEngine:
    # 1. PII Regex patterns
    PAN_PATTERN = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", re.IGNORECASE)
    AADHAAR_PATTERN = re.compile(r"\b[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}\b")
    EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
    PHONE_PATTERN = re.compile(r"\b(?:\+?\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}\b")
    
    # 2. Advice Refusal keywords
    ADVICE_KEYWORDS = [
        "should i invest", "should i buy", "is it good", "which is better",
        "which fund to choose", "recommend", "opinion", "suggest a fund",
        "where to put my money", "best fund", "top fund", "portfolio advice"
    ]
    
    # 3. Performance / Projection keywords
    PERFORMANCE_KEYWORDS = [
        "return", "performance", "future growth", "projection", "predict",
        "estimate", "historical return", "cagr", "dividend payout", "nav history",
        "how much will i make", "past performance"
    ]

    def check_pre_retrieval(self, query: str) -> Tuple[bool, Optional[str]]:
        """
        Run checks on the raw user query before retrieving documents.
        Returns:
            (is_safe, error_or_refusal_message)
        """
        # A. Check PII
        if self.PAN_PATTERN.search(query):
            return False, "Query blocked: Please do not share sensitive personal identifiers like PAN card numbers."
        if self.AADHAAR_PATTERN.search(query):
            return False, "Query blocked: Please do not share sensitive personal identifiers like Aadhaar card numbers."
        if self.EMAIL_PATTERN.search(query):
            return False, "Query blocked: Please do not share sensitive personal identifiers like email addresses."
        if self.PHONE_PATTERN.search(query):
            return False, "Query blocked: Please do not share sensitive personal identifiers like phone numbers."
            
        # B. Check Investment Advice Refusal
        query_lower = query.lower()
        if any(kw in query_lower for kw in self.ADVICE_KEYWORDS):
            return False, (
                "I am a facts-only assistant and do not provide investment advice or recommendations. "
                "Please refer to the official scheme document details or consult a certified financial advisor. "
                "You can read more about mutual funds on the [AMFI Investor Education Page](https://www.amfiindia.com/investor-corner/knowledge-center/what-are-mutual-funds.html)."
            )
            
        # C. Check Performance Refusal (returns, cagr, performance)
        if any(kw in query_lower for kw in self.PERFORMANCE_KEYWORDS):
            return False, (
                "I am a facts-only assistant and do not provide past performance statistics, returns projections, "
                "or comparisons. For official performance figures, please download and consult the official scheme factsheets "
                "available on the [SBI Mutual Fund Factsheets Page](https://www.sbimf.com/factsheets)."
            )
            
        return True, None

    def enforce_citations(self, response_text: str, retrieved_docs: List[Document]) -> str:
        """
        Ensure the response contains a valid source citation URL.
        If the LLM failed to include one, append the top-ranked source URL from the retrieved documents.
        """
        # Check if response already has a link
        if "http://" in response_text or "https://" in response_text:
            return response_text
            
        # If no link, find the first valid source URL in retrieved documents
        for doc in retrieved_docs:
            url = doc.metadata.get("source_url")
            if url:
                # Append to response
                cleaned_url = url.strip()
                response_text += f"\n\nSource: [Official Scheme Factsheet]({cleaned_url})"
                break
                
        return response_text

# Singleton instance
guardrails_instance = None

def get_guardrails():
    global guardrails_instance
    if guardrails_instance is None:
        guardrails_instance = GuardrailsEngine()
    return guardrails_instance
