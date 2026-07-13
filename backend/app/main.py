import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Ensure the backend directory is in the path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Load env variables on startup
load_dotenv(os.path.join(backend_dir, ".env"))

from app.core.config import settings
from app.routers import chat

app = FastAPI(
    title="RAG Mutual Fund FAQ Chatbot Backend",
    description="FastAPI Backend serving mutual fund factsheet queries with citations and safety guardrails.",
    version="1.0.0"
)

# 1. Provide safe default origins for local dev and the specific Vercel frontend
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://rag-based-mutual-fund-faq-chatbot-sage.vercel.app"
]

# 2. Append any origins passed via environment variables
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env and allowed_origins_env != "*":
    default_origins.extend([o.strip() for o in allowed_origins_env.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=default_origins,
    allow_origin_regex=r"https://rag-based-mutual-fund-faq-chatbot.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to the RAG Mutual Fund FAQ API. Use /api/chat to query."
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
