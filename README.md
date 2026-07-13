# RAG-based Mutual Fund FAQ Chatbot

> **Facts-only AI assistant** for SBI Mutual Fund scheme inquiries — powered by FAISS vector search, Groq LLaMA, and a premium Next.js UI inspired by INDMoney's dark-mode aesthetic.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white) ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white) ![Groq](https://img.shields.io/badge/Groq_LLaMA-orange?style=flat) ![FAISS](https://img.shields.io/badge/FAISS-blue?style=flat)

**Live Demo (Frontend):** [https://rag-based-mutual-fund-faq-chatbot-sage.vercel.app/](https://rag-based-mutual-fund-faq-chatbot-sage.vercel.app/)  
**Live API (Backend):** [https://rag-based-mutual-fund-faq-chatbot-ch45.onrender.com/docs](https://rag-based-mutual-fund-faq-chatbot-ch45.onrender.com/docs)
---

## 📌 What This Project Does

This chatbot answers **factual questions** about 6 SBI Mutual Fund schemes by performing:

1. **Pre-Retrieval Guardrails** — Blocks PII inputs (PAN, Aadhaar, email, phone), investment advice queries, and performance/returns comparisons.
2. **FAISS Vector Retrieval** — Finds top-3 semantically relevant chunks from local HTML factsheets using BAAI/bge-small-en-v1.5 embeddings.
3. **LLM Generation (Groq)** — Generates concise, factual answers (≤3 sentences) using `llama-3.3-70b-versatile` with strict system instructions.
4. **Citation Enforcement** — Every response contains a clickable source URL with `Last Updated` date from the factsheet metadata.

---

## 🗂️ Scoped Schemes

| Scheme | Category | Risk |
|---|---|---|
| SBI Bluechip Fund | Equity — Large Cap | Very High |
| SBI Flexicap Fund | Equity — Flexi Cap | Very High |
| SBI Long Term Equity Fund (ELSS) | Equity — Tax Saver | Very High |
| SBI Small Cap Fund | Equity — Small Cap | Very High |
| SBI Contra Fund | Equity — Contra | Very High |
| SBI Liquid Fund | Debt — Liquid | Low to Moderate |

---

## 🏗️ Architecture

```
User Browser (Next.js @ Vercel)
        │
        │  POST /api/chat { question, scheme }
        ▼
FastAPI Backend (Render)
   ├── GuardrailsEngine  ← PII + Advice pre-filter
   ├── FAISSRetriever    ← BAAI/bge embeddings + faiss-cpu
   ├── RAGChain          ← Groq LLaMA-3.3-70b
   └── Citation Enforcer ← Post-generation source check
        │
        │  { answer, retrieved_chunks: [{source_url, date_accessed, ...}] }
        ▼
User Browser — renders response + citation pills
```

---

## 🛠️ Tech Stack Decision Log

| Component | Choice | Reason |
|---|---|---|
| **LLM** | Groq Cloud `llama-3.3-70b-versatile` | Free tier, 500+ tok/s, excellent instruction following |
| **Vector DB** | FAISS (`faiss-cpu`) | In-process, disk-persisted, no RAM/cost overhead on Render Free |
| **Embeddings (Local)** | `sentence-transformers` BAAI/bge-small-en-v1.5 | Offline during ingestion/development |
| **Embeddings (Prod)** | `HuggingFaceInferenceAPIEmbeddings` | No PyTorch in production, stays within 512MB RAM |
| **Backend** | FastAPI + Uvicorn | Async, fast, OpenAPI docs auto-generated |
| **Frontend** | Next.js (App Router) | React server components, easy Vercel deployment |
| **Styling** | Vanilla CSS (CSS variables) | Zero runtime overhead; INDMoney dark-mode design |

---

## 📁 Project Structure

```
RAG-based-Mutual-Fund-FAQ-Chatbot/
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── core/
│   │   │   ├── config.py            # Pydantic settings (env vars)
│   │   │   └── embeddings.py        # Hybrid local/hosted embeddings
│   │   ├── routers/
│   │   │   └── chat.py              # POST /api/chat endpoint
│   │   └── services/
│   │       ├── retriever.py         # FAISSRetriever (singleton)
│   │       ├── chain.py             # RAGChain with Groq LLaMA
│   │       └── guardrails.py        # PII + advice + citation enforcer
│   ├── ingestion/
│   │   ├── parser.py                # HTML/PDF → LangChain Document
│   │   └── ingest.py                # Embeds docs → FAISS index
│   ├── data/
│   │   ├── raw/                     # HTML factsheets (committed to Git)
│   │   └── vectorstore/             # FAISS index (committed to Git)
│   ├── Dockerfile                   # Production Docker image for Render
│   ├── requirements.txt             # Production Python deps (no torch)
│   └── .env.example                 # Template for environment variables
│
├── frontend/
│   └── src/
│       ├── app/
│       │   ├── layout.js            # Root layout + SEO metadata
│       │   ├── page.js              # Main chat page (wires all components)
│       │   └── globals.css          # Full Vanilla CSS design system
│       ├── components/
│       │   ├── Header.jsx           # App title + API status indicator
│       │   ├── DisclaimerBanner.jsx # Facts-only warning ribbon
│       │   ├── SchemeSelector.jsx   # Fund selector sidebar cards
│       │   ├── SuggestionChips.jsx  # Contextual query suggestion pills
│       │   ├── ChatWindow.jsx       # Message list + typing indicator
│       │   └── InputBar.jsx         # Input form with send button
│       └── lib/
│           └── api.js               # fetch wrapper → FastAPI backend
│
├── docs/
│   ├── implementation.md            # Phase-by-phase build plan
│   ├── architecture.md              # System design diagrams
│   ├── schemes.md                   # Fund scope and details
│   ├── sources.md                   # 18 verified source URLs
│   └── sample_qa.md                 # Example responses & refusals
│
└── README.md
```

---

## 🚀 Local Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A free **Groq API key** from [console.groq.com](https://console.groq.com)
- A free **Hugging Face token** from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) *(for production)*

---

### Backend Setup (FastAPI)

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install ALL dependencies (includes sentence-transformers for local embeddings)
pip install -r requirements.txt
pip install sentence-transformers  # Local dev only — not included in prod

# Set up environment variables
copy .env.example .env      # Windows
# cp .env.example .env      # macOS/Linux

# Edit backend/.env — add your keys:
# GROQ_API_KEY=gsk_...
# HF_TOKEN=hf_...
```

**Run the ingestion pipeline** (only needed once, or when factsheets change):
```bash
python -m ingestion.ingest
```
This generates `backend/data/vectorstore/index.faiss` and `index.pkl`.

**Start the API:**
```bash
uvicorn app.main:app --reload
# → http://localhost:8000
# → Swagger UI: http://localhost:8000/docs
```

---

### Frontend Setup (Next.js)

```bash
cd frontend

npm install

# Create local env file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
# → http://localhost:3000
```

---

## 🌐 Production Deployment

### Backend → Render (Docker)

1. Push the full repo to GitHub (including `backend/data/vectorstore/`).
2. Create a **New Web Service** on [render.com](https://render.com).
3. Connect your GitHub repository.
4. Render will detect the `backend/Dockerfile` automatically via `render.yaml`.
5. Add the following **Environment Variables** in Render dashboard:
   - `GROQ_API_KEY` — your Groq API key
   - `HF_TOKEN` — your HuggingFace token
   - `ALLOWED_ORIGINS` — your Vercel frontend URL (e.g. `https://your-app.vercel.app`)

### Frontend → Vercel

1. Go to [vercel.com](https://vercel.com) and import your GitHub repository.
2. Set the **Root Directory** to `frontend`.
3. Add the **Environment Variable**:
   - `NEXT_PUBLIC_API_URL` — your Render backend URL (e.g. `https://your-api.onrender.com`)
4. Deploy. Vercel auto-detects Next.js and builds correctly.

---

## 🛡️ Guardrail Rules

| Rule | Trigger | Response |
|---|---|---|
| **PII Block** | PAN, Aadhaar, email, phone in query | Immediate refusal, no retrieval |
| **Advice Refusal** | "Should I invest", "recommend", "best fund" | Redirected to AMFI Investor Education |
| **Performance Block** | "CAGR", "return", "past performance" | Redirected to official SBI factsheet page |
| **Citation Enforcer** | Response lacks a source URL | Source URL appended from top retrieved chunk |

---

## 📄 API Reference

### `POST /api/chat`

**Request body:**
```json
{
  "question": "What is the exit load for SBI Small Cap Fund?",
  "scheme": "SBI Small Cap Fund"
}
```

**Response body:**
```json
{
  "answer": "For SBI Small Cap Fund, an exit load of 1.00% applies for redemptions within 1 year...",
  "retrieved_chunks": [
    {
      "content": "...",
      "source_url": "https://www.sbimf.com/...",
      "scheme_name": "SBI Small Cap Fund",
      "document_type": "factsheet",
      "date_accessed": "June 1, 2026",
      "title": "SBI Small Cap Fund — Scheme Factsheet"
    }
  ]
}
```

See [sample_qa.md](./docs/sample_qa.md) for example responses and refusals.

---

## 📝 License

This project is built for educational purposes and portfolio demonstration. All mutual fund factsheet data sourced from [sbimf.com](https://www.sbimf.com) is the property of SBI Funds Management Ltd.
