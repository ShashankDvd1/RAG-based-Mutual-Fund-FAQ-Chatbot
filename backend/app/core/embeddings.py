import os
from app.core.config import settings

def get_embeddings():
    """
    Return embeddings. Uses local HuggingFaceEmbeddings if sentence-transformers is installed
    (for offline local development/testing), otherwise falls back to hosted
    HuggingFaceInferenceAPIEmbeddings (for production on Render).
    """
    try:
        import sentence_transformers
        from langchain_huggingface import HuggingFaceEmbeddings
        print(f"Loading local embedding model: {settings.EMBEDDING_MODEL} (development mode)...")
        return HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
    except ImportError:
        print(f"Loading hosted embedding model: {settings.EMBEDDING_MODEL} (production mode)...")
        from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
        
        # Fallback URL if api-inference.huggingface.co is blocked/unresolvable
        api_url = None
        try:
            import socket
            socket.getaddrinfo('api-inference.huggingface.co', 443)
        except Exception:
            api_url = f"https://router.huggingface.co/hf-inference/models/{settings.EMBEDDING_MODEL}"

        api_key = settings.HF_TOKEN.strip() if settings.HF_TOKEN else ""
        return HuggingFaceInferenceAPIEmbeddings(
            api_key=api_key,
            model_name=settings.EMBEDDING_MODEL,
            api_url=api_url
        )
