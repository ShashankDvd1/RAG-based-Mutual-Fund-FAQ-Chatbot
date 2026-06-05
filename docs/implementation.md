# RAG-based Mutual Fund FAQ Chatbot — Implementation Plan

> Phase-wise breakdown derived from [problemstatement.md](./problemstatement.md)

---

## Phase 1 — Project Setup & Product / AMC Selection

### Objective
Bootstrap the repository, configure INDMoney-branded tech choices, and finalise the SBI Mutual Fund schemes.

### Tasks

| # | Task | Details |
|---|---|---|
| 1.1 | **Select product** | **Locked in:** INDMoney (Premium dark-mode personal finance app theme). |
| 1.2 | **Select AMC & schemes** | **Locked in:** SBI Mutual Fund. Selected 6 schemes:<br/>1. SBI Bluechip Fund (Large Cap)<br/>2. SBI Flexicap Fund (Flexi Cap)<br/>3. SBI Long Term Equity Fund (ELSS / Lock-in)<br/>4. SBI Small Cap Fund (Small Cap)<br/>5. SBI Contra Fund (Contra)<br/>6. SBI Liquid Fund (Liquid/Debt) |
| 1.3 | **Initialise repository** | Create folder structure, virtual environment, `requirements.txt`, `.env.example`. |
| 1.4 | **Choose tech stack** | **Frontend:** Next.js (React) deployed on **Vercel**. **Backend:** FastAPI (Python) deployed on **Render**. **LLM:** Groq (Llama 3 / Mixtral via Groq Cloud — ultra-fast inference). Vector DB: FAISS / ChromaDB. |
| 1.5 | **Add `.gitignore`** | Exclude `.env`, `__pycache__`, vector-store artefacts, etc. |

### Proposed Folder Structure

```
RAG-based-Mutual-Fund-FAQ-Chatbot/
├── frontend/                    # Next.js app → deployed on Vercel
│   ├── public/                  # Static assets (icons, images)
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── components/          # React UI components
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── SuggestionChip.jsx
│   │   │   ├── DisclaimerBanner.jsx
│   │   │   └── Header.jsx
│   │   ├── hooks/               # Custom React hooks
│   │   ├── lib/                 # API client, utilities
│   │   └── styles/              # Global CSS, design tokens
│   ├── .env.local.example
│   ├── next.config.js
│   ├── package.json
│   └── vercel.json
│
├── backend/                     # FastAPI server → deployed on Render
│   ├── app/
│   │   ├── main.py              # FastAPI entry point + CORS
│   │   ├── routers/
│   │   │   └── chat.py          # /api/chat endpoint
│   │   ├── services/
│   │   │   ├── retriever.py     # Vector store query logic
│   │   │   ├── chain.py         # RAG chain (prompt + LLM)
│   │   │   └── guardrails.py    # PII filter, advice refusal, citation enforcer
│   │   └── core/
│   │       ├── config.py        # Settings / env vars
│   │       └── embeddings.py    # Embedding model wrapper
│   ├── ingestion/               # Scraping & chunking scripts
│   ├── data/
│   │   ├── raw/                 # Downloaded HTML / PDF pages
│   │   └── vectorstore/         # Persisted FAISS / ChromaDB index
│   ├── .env.example
│   ├── requirements.txt
│   ├── Dockerfile               # For Render deployment
│   └── render.yaml              # Render service config
│
├── docs/
│   ├── problemstatement.md
│   ├── implementation.md
│   ├── sources.md               # 15–25 URLs list
│   └── sample_qa.md             # 5–10 sample Q&A pairs
└── README.md
```

### Deliverables
- Working repo with empty folder skeleton.
- `requirements.txt` with initial dependencies.
- Decision log (AMC, schemes, tech stack) documented in `README.md`.

---

## Phase 2 — Data Collection & Source Cataloguing

### Objective
Gather 15–25 official public pages and build the source list.

### Tasks

| # | Task | Details |
|---|---|---|
| 2.1 | **Identify URLs** | Collect factsheets, KIM/SID PDFs, scheme FAQ pages, fee/charges pages, riskometer/benchmark notes, statement/tax-doc guides from the chosen AMC, SEBI, and AMFI websites. |
| 2.2 | **Download & archive** | Save each page as HTML or PDF into `data/raw/` with a clear naming convention (e.g., `sbi_bluechip_factsheet_jun2026.pdf`). |
| 2.3 | **Create `sources.md`** | Tabulate all URLs with columns: `#`, `URL`, `Page Title`, `Type` (factsheet / KIM / FAQ / …), `Date Accessed`. |
| 2.4 | **Validate sources** | Ensure every URL is an official AMC / SEBI / AMFI page — no third-party blogs. |

### Source Types Checklist

- [ ] Scheme factsheets (one per scheme, latest month)
- [ ] KIM / SID documents
- [ ] AMC scheme-specific FAQ pages
- [ ] Fee & charges / exit-load tables
- [ ] Riskometer classification & benchmark pages
- [ ] Account-statement / capital-gains download guides
- [ ] AMFI scheme-search / NAV pages
- [ ] SEBI mutual-fund regulation / investor-education pages

### Deliverables
- `data/raw/` populated with 15–25 files.
- `docs/sources.md` with the complete URL catalogue.

---

## Phase 3 — Data Processing & Vector Store Creation

### Objective
Parse, clean, chunk the collected documents and build the vector store for retrieval.

### Tasks

| # | Task | Details |
|---|---|---|
| 3.1 | **Parse documents** | Extract text from HTML (BeautifulSoup) and PDF (PyPDF2 / pdfplumber). |
| 3.2 | **Clean text** | Remove headers, footers, navigation chrome, disclaimers, and boilerplate. Normalise whitespace. |
| 3.3 | **Chunk text** | Split into overlapping chunks (e.g., 500 tokens, 100-token overlap) using LangChain's `RecursiveCharacterTextSplitter`. |
| 3.4 | **Attach metadata** | Tag every chunk with: `source_url`, `scheme_name`, `document_type`, `date_accessed`. |
| 3.5 | **Generate embeddings** | Use an embedding model (e.g., HuggingFace `sentence-transformers/all-MiniLM-L6-v2` for local/free embeddings, or OpenAI `text-embedding-ada-002` if budget allows) to embed each chunk. *Note: Groq does not provide an embedding API — use a separate embedding provider.* |
| 3.6 | **Store in vector DB** | Persist embeddings + metadata in FAISS / ChromaDB. Save the index to `data/processed/`. |

### Key Design Decisions

- **Chunk size & overlap:** Start with 500 / 100; tune later based on retrieval quality.
- **Metadata is critical:** The `source_url` field in metadata powers the citation requirement.

### Deliverables
- Ingestion pipeline scripts in `src/ingestion/`.
- Persisted vector store in `data/processed/`.
- Embedding + indexing script that can be re-run on new data.

---

## Phase 4 — RAG Retrieval Chain & Guardrails (Groq LLM)

### Objective
Build the core question-answering pipeline with retrieval, **Groq-powered generation**, citations, and safety guardrails.

### Why Groq?

| Feature | Details |
|---|---|
| **Speed** | Groq's LPU (Language Processing Unit) delivers ~500+ tokens/sec — near-instant responses for the chatbot. |
| **Models** | Access to `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768` via the Groq Cloud API. |
| **Free tier** | Generous free-tier rate limits — ideal for prototyping and demos. |
| **LangChain integration** | `langchain-groq` package provides `ChatGroq` class — drop-in replacement. |
| **API compatibility** | OpenAI-compatible REST API — easy to switch models later if needed. |

### Tasks

| # | Task | Details |
|---|---|---|
| 4.1 | **Build retriever** | Query the vector store with the user's question; retrieve top-k (e.g., k=3) relevant chunks along with their metadata. |
| 4.2 | **Construct prompt template** | Design a system prompt that instructs the LLM to: answer in ≤ 3 sentences, include exactly one source link from the retrieved metadata, and append `"Last updated from sources: <date>"`. |
| 4.3 | **Implement advice refusal** | Add a pre-check (keyword / classifier) to detect opinionated or portfolio questions. If detected, return a polite refusal message + an educational link (e.g., AMFI investor-education page). |
| 4.4 | **Implement PII filter** | Add input validation to reject or redact PAN, Aadhaar, account numbers, OTPs, emails, and phone numbers before they reach the LLM. |
| 4.5 | **Implement performance-claim guard** | If the query asks about returns / past performance / comparison, return a refusal + link to the official factsheet instead. |
| 4.6 | **Citation enforcer** | Post-process the LLM response to verify a valid source URL is present; if missing, inject the top-ranked chunk's `source_url`. |

### Prompt Template (Sketch)

```python
# backend/app/services/chain.py (sketch)
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

llm = ChatGroq(
    model="llama-3.3-70b-versatile",   # or "llama-3.1-8b-instant" for faster responses
    temperature=0,
    api_key=GROQ_API_KEY,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a facts-only mutual fund FAQ assistant for [Product].
Use ONLY the provided context to answer. Do NOT give investment advice.

Rules:
1. Answer in 3 sentences or fewer.
2. Include exactly one source link from the context metadata.
3. End with "Last updated from sources: <date>".
4. If the question asks for advice, opinions, or performance projections,
   politely refuse and provide this educational link: [AMFI link]."""),
    ("human", "Context:\n{context}\n\nQuestion: {question}"),
])

chain = prompt | llm
```

### Deliverables
- RAG chain module in `backend/app/services/` using `langchain-groq`.
- Guardrail modules in `backend/app/services/guardrails.py` (PII filter, advice refusal, citation enforcer).
- Unit tests / manual test log for each guardrail.

### Key Dependencies (Backend)

```txt
# requirements.txt (Phase 4 additions)
langchain>=0.2
langchain-groq>=0.1
langchain-community>=0.2
faiss-cpu>=1.7
sentence-transformers>=2.2
fastapi>=0.111
uvicorn>=0.30
python-dotenv>=1.0
```

---

## Phase 5 — Premium Frontend UI (Next.js + Vercel)

### Objective
Build a **production-grade, visually stunning** chatbot frontend in Next.js that feels premium and modern — not a basic Streamlit/Gradio app.

### Architecture

```
┌──────────────────────┐         ┌──────────────────────┐
│   Next.js Frontend   │  HTTPS  │   FastAPI Backend     │
│   (Vercel)           │ ──────► │   (Render)            │
│                      │  JSON   │                       │
│  • React components  │ ◄────── │  • /api/chat endpoint │
│  • Client-side state │         │  • RAG chain          │
│  • Animations / CSS  │         │  • Guardrails         │
└──────────────────────┘         └──────────────────────┘
```

### Tasks

| # | Task | Details |
|---|---|---|
| 5.1 | **Initialise Next.js app** | `npx -y create-next-app@latest ./frontend` with App Router, ESLint, vanilla CSS. |
| 5.2 | **Design system & tokens** | Define CSS custom properties: colour palette, typography (Google Font — Inter / Outfit), spacing scale, border-radius, shadows, glassmorphism variables. |
| 5.3 | **Dark-mode theme** | Default dark background with subtle gradients. Charcoal / deep black base (`hsl(215, 28%, 8%)`) with neon green / teal accents (`hsl(150, 95%, 43%)`) inspired by **INDMoney**. |
| 5.4 | **Header component** | App logo/icon + title + subtle animated glow / gradient text with INDMoney styling. |
| 5.5 | **Disclaimer banner** | Persistent glassmorphic banner: **"Facts-only. No investment advice."** with an info icon and frosted-glass effect. |
| 5.6 | **Scheme Selector Panel** | Interactive left sidebar (desktop) or horizontal sliding cards (mobile) listing the 6 scoped schemes. Selecting a scheme highlights it, shows its category/riskometer badge, and binds the chatbot context to that scheme. |
| 5.7 | **Suggestion chips** | 3 context-aware suggestion question buttons based on the selected scheme (e.g., "What is the exit load?", "Show minimum SIP") that auto-fill the input. |
| 5.8 | **Chat window** | Scrollable message area with distinct user / bot bubbles. Bot bubbles use a subtle gradient background. Auto-scroll to latest. |
| 5.9 | **Message bubbles** | Rounded cards with: avatar icon, message text, citation link styled as a pill badge, "Last updated" timestamp in muted text. |
| 5.10 | **Typing indicator** | Animated dot-pulse loader while waiting for the backend response. |
| 5.11 | **Input bar** | Fixed-bottom input with a frosted-glass backdrop, rounded corners, a send-button with hover scale animation. Sends selected scheme alongside user query. |
| 5.12 | **Micro-animations** | Fade-in for new messages, scale-up on card/chip hover, smooth transitions on scheme selection changes, subtle entrance animation. |
| 5.13 | **Responsive layout** | Fluid split-pane layout: Sidebar + Chat area on desktop; vertical stacking with sliding selector on mobile. |
| 5.14 | **API integration** | `fetch` / custom hook to call the backend `POST /api/chat` sending `{ question, scheme }`. Handle loading, error, and empty states gracefully. |
| 5.15 | **SEO & meta** | Proper `<title>`, `<meta description>`, Open Graph tags, favicon. |

### Visual Design Direction

- **Colour palette:** Dark mode — `hsl(215, 28%, 8%)` background, `hsl(215, 21%, 15%)` card backgrounds, `hsl(150, 95%, 43%)` accent (INDMoney-inspired neon green/teal), white/grey text.
- **Typography:** Google Font `Inter` (body) + `Outfit` (headings) — clean, modern, premium.
- **Glassmorphism:** Frosted-glass cards with `backdrop-filter: blur(12px)`, subtle translucent borders, and soft shadows.
- **Gradients:** Subtle radial ambient glow in background corners; neon green linear gradient hover states.
- **Animations:** CSS `@keyframes` for fade-in, slide-up, pulse, and spring transitions on selected schemes.

### UI Wireframe (Text)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│   ✦  INDMoney MF FAQ Assistant                                  [🌙 Dark]   │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ ℹ️ Facts-only assistant. No investment advice. Official SBI MF facts.   │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│ ┌───────────────────────────┬─────────────────────────────────────────────┐ │
│ │ 🗂️ SELECT SCHEME         │ 💬 CHAT WINDOW                              │ │
│ │ ┌───────────────────────┐ │ ┌─────────────────────────────────────────┐ │ │
│ │ │ 🟢 SBI Bluechip Fund  │ │ │ 🧑 User: What is the exit load?         │ │ │
│ │ │    Large Cap          │ │ │                                         │ │ │
│ │ ├───────────────────────┤ │ │ 🤖 Bot: The exit load is 1% if redeemed  │ │ │
│ │ │ ⚪ SBI Flexicap Fund  │ │ │         within 1 year of allotment.     │ │ │
│ │ │    Flexi Cap          │ │ │         🔗 Source: [Official Factsheet]  │ │ │
│ │ ├───────────────────────┤ │ │         Last updated: Jun 2026          │ │ │
│ │ │ ⚪ SBI Long Term ELSS │ │ └─────────────────────────────────────────┘ │ │
│ │ │    Lock-in (3 Years)  │ │ Suggestion:                                 │ │
│ │ ├───────────────────────┤ │ ┌───────────────────┐ ┌──────────────────┐  │ │
│ │ │ ⚪ SBI Small Cap Fund │ │ │ Show expense ratio│ │ What is min SIP? │  │ │
│ │ │    Small Cap          │ │ └───────────────────┘ └──────────────────┘  │ │
│ │ ├───────────────────────┤ │                                             │ │
│ │ │ ⚪ SBI Contra Fund    │ │ ┌─────────────────────────────────────┐ ┌──┐│ │
│ │ │    Contra             │ │ │ Type a question about SBI Bluechip... │ │➤ ││ │
│ │ └───────────────────────┘ │ └─────────────────────────────────────┘ └──┘│ │
│ └───────────────────────────┴─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Deliverables
- Complete Next.js app in `frontend/` with all components.
- Polished, responsive, dark-mode UI with micro-animations.
- Screenshots of the running UI for README / demo video.

---

## Phase 6 — Testing, Sample Q&A & Documentation

### Objective
Validate the end-to-end system and prepare all submission deliverables.

### Tasks

| # | Task | Details |
|---|---|---|
| 6.1 | **Functional testing** | Run 10+ queries covering: factual answers, advice refusal, PII rejection, performance-claim refusal, citation presence. |
| 6.2 | **Create `sample_qa.md`** | Document 5–10 queries with the assistant's actual responses and citation links. Include at least 1 refusal example. |
| 6.3 | **Write `README.md`** | Cover: project overview, selected product + AMC + schemes, setup steps (backend: `pip install` + `uvicorn`; frontend: `npm install` + `npm run dev`), env vars, deployment URLs (Vercel + Render), known limitations. |
| 6.4 | **Finalise `sources.md`** | Confirm all 15–25 URLs are valid and accessible. |
| 6.5 | **Add disclaimer snippet** | Document the exact disclaimer text and its placement in the UI. |
| 6.6 | **Edge-case testing** | Test: empty input, very long input, mixed PII + valid question, non-MF question, non-English input. |

### Sample Q&A Scenarios

| # | Query Type | Example Query |
|---|---|---|
| 1 | Factual — Expense Ratio | *"What is the expense ratio of SBI Bluechip Fund?"* |
| 2 | Factual — Exit Load | *"What is the exit load for SBI Focused Equity Fund?"* |
| 3 | Factual — Lock-in | *"Does ELSS have a lock-in period?"* |
| 4 | Factual — Minimum SIP | *"What is the minimum SIP amount?"* |
| 5 | Factual — Riskometer | *"What is the riskometer category and benchmark?"* |
| 6 | Factual — Statements | *"How do I download my capital gains statement?"* |
| 7 | Refusal — Advice | *"Should I invest in this fund?"* |
| 8 | Refusal — Performance | *"What were the 5-year returns?"* |
| 9 | Refusal — PII | *"My PAN is ABCDE1234F, show my portfolio."* |
| 10 | Refusal — Comparison | *"Which fund is better, X or Y?"* |

### Deliverables
- `docs/sample_qa.md`
- Final `README.md`
- Final `docs/sources.md`
- All guardrail tests passing.

---

## Phase 7 — Deployment (Vercel + Render) & Submission

### Objective
Deploy frontend to **Vercel**, backend to **Render**, and package all deliverables.

### Tasks

| # | Task | Details |
|---|---|---|
| 7.1 | **Deploy backend to Render** | Create a Render Web Service from the `backend/` directory. Use the `Dockerfile` or Render's native Python runtime. Set env vars (`GROQ_API_KEY`, etc.) in Render dashboard. Free tier is fine. |
| 7.2 | **Deploy frontend to Vercel** | Connect the GitHub repo to Vercel. Set root directory to `frontend/`. Add env var `NEXT_PUBLIC_API_URL` pointing to the Render backend URL. |
| 7.3 | **Configure CORS** | Ensure the FastAPI backend allows requests from the Vercel frontend domain. |
| 7.4 | **Smoke test production** | Verify the full flow end-to-end on the live URLs: factual query → citation, advice refusal, PII rejection. |
| 7.5 | **Record demo** | Record a ≤ 3-min walkthrough video as a backup, showing: welcome UI, example queries, factual answers with citations, advice refusal, PII rejection. |
| 7.6 | **Final review** | Walk through the deliverables checklist one last time. |
| 7.7 | **Submit** | Share: Vercel prototype link, Render API URL, source list, README, sample Q&A, disclaimer snippet. |

### Deployment Topology

```
┌──────────────┐      HTTPS / JSON       ┌───────────────┐
│              │  ──────────────────────► │               │
│   Vercel     │                          │   Render      │
│   (Next.js)  │  ◄────────────────────── │   (FastAPI)   │
│              │                          │               │
│  frontend/   │                          │  backend/     │
│  Static +    │                          │  Python API + │
│  Client JS   │                          │  Vector Store │
└──────────────┘                          └───────────────┘
     ▲                                          ▲
     │  Custom domain (optional)                │  Render URL
     │  https://mf-faq.vercel.app               │  https://mf-faq-api.onrender.com
```

### Render Configuration (`render.yaml`)

```yaml
services:
  - type: web
    name: mf-faq-backend
    runtime: python
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GROQ_API_KEY
        sync: false
```

### Vercel Configuration (`vercel.json`)

```json
{
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

### Submission Checklist

- [ ] **Vercel link** — Live frontend URL
- [ ] **Render link** — Live backend API URL
- [ ] Working prototype link **or** ≤ 3-min demo video
- [ ] `docs/sources.md` — 15–25 official URLs
- [ ] `README.md` — Setup steps, scope (AMC + schemes), deployment URLs, known limits
- [ ] `docs/sample_qa.md` — 5–10 queries with answers + links
- [ ] Disclaimer snippet visible in the UI

---

## Timeline Overview

| Phase | Description | Estimated Effort |
|---|---|---|
| **Phase 1** | Project Setup & Selections | 1–2 hours |
| **Phase 2** | Data Collection & Source List | 2–3 hours |
| **Phase 3** | Data Processing & Vector Store | 3–4 hours |
| **Phase 4** | RAG Chain & Guardrails | 4–5 hours |
| **Phase 5** | Premium Frontend UI (Next.js) | 4–6 hours |
| **Phase 6** | Testing & Documentation | 2–3 hours |
| **Phase 7** | Deployment (Vercel + Render) & Submission | 2–3 hours |
| | **Total** | **~18–26 hours** |
