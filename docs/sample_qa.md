# Sample Q&A — RAG Mutual Fund FAQ Chatbot

This document contains representative examples of queries and responses from the SBI Mutual Fund FAQ Chatbot, covering both successful factual retrievals and guardrail refusals.

---

## ✅ Factual Retrieval Examples

### Q1 — Exit Load (SBI Small Cap Fund)

**User Query:** `What is the exit load for SBI Small Cap Fund?`

**Scheme Context:** SBI Small Cap Fund

**Expected Response:**
> For SBI Small Cap Fund, an exit load of **1.00%** of the applicable NAV is charged for redemption or switch-out of units within **1 year (365 days)** from the date of allotment. After 1 year, no exit load is applicable.
>
> Source: [Official Scheme Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-small-cap-fund-329)

---

### Q2 — SIP Subscription Limits (SBI Small Cap Fund)

**User Query:** `Can I do a lumpsum investment in SBI Small Cap Fund?`

**Scheme Context:** SBI Small Cap Fund

**Expected Response:**
> Due to high inflows, lumpsum investments in SBI Small Cap Fund are currently **suspended**. Fresh investments can only be made through Systematic Investment Plans (SIPs), capped at a maximum of **Rs. 25,000 per PAN per month**. Minimum SIP installment is Rs. 500 (monthly), with a minimum of 6 installments required.
>
> Source: [Official Scheme Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-small-cap-fund-329)

---

### Q3 — Exit Load Tiered Structure (SBI Liquid Fund)

**User Query:** `What is the exit load for SBI Liquid Fund?`

**Scheme Context:** SBI Liquid Fund

**Expected Response:**
> SBI Liquid Fund applies a tiered exit load for redemptions within 7 days of allotment. The charges are: Day 1 → 0.0070%, Day 2 → 0.0065%, Day 3 → 0.0060%, Day 4 → 0.0055%, Day 5 → 0.0050%, Day 6 → 0.0045%, and **Day 7 onwards → Nil**. No exit load applies from Day 7 onwards.
>
> Source: [Official Scheme Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-liquid-fund-19)

---

### Q4 — Lock-in Period (SBI Long Term Equity Fund / ELSS)

**User Query:** `Is there a lock-in period for SBI Long Term Equity Fund?`

**Scheme Context:** SBI Long Term Equity Fund

**Expected Response:**
> Yes. SBI Long Term Equity Fund (ELSS) has a mandatory **3-year lock-in period** from the date of allotment of each installment. It qualifies for tax deductions under **Section 80C** of the Income Tax Act, up to Rs. 1,50,000 per year. The benchmark is the S&P BSE 500 TRI.
>
> Source: [Official Scheme Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-elss-tax-saver-fund-(formerly-known-as-sbi-long-term-equity-fund)-3)

---

### Q5 — Fund Manager (SBI Liquid Fund)

**User Query:** `Who manages SBI Liquid Fund?`

**Scheme Context:** SBI Liquid Fund

**Expected Response:**
> SBI Liquid Fund is managed by **Mr. Sandeep Agarwal** (since October 2022) and **Mr. Rohit Kumar** (since July 2024).
>
> Source: [Official Scheme Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-liquid-fund-19)

---

## 🚫 Guardrail Refusal Examples

### R1 — Investment Advice Refusal

**User Query:** `Should I invest in SBI Small Cap Fund right now?`

**Expected Response (Guardrail):**
> I am a facts-only assistant and do not provide investment advice or recommendations. Please refer to the official scheme document details or consult a certified financial advisor. You can read more about mutual funds on the [AMFI Investor Education Page](https://www.amfiindia.com/investor-corner/knowledge-center/what-are-mutual-funds.html).

---

### R2 — PII / PAN Card Refusal

**User Query:** `My PAN is ABCDE1234F. Can you check my portfolio?`

**Expected Response (Guardrail):**
> Query blocked: Please do not share sensitive personal identifiers like PAN card numbers.

---

### R3 — Past Performance / Returns Refusal

**User Query:** `What is the 5-year CAGR of SBI Bluechip Fund?`

**Expected Response (Guardrail):**
> I am a facts-only assistant and do not provide past performance statistics, returns projections, or comparisons. For official performance figures, please download and consult the official scheme factsheets available on the [SBI Mutual Fund Factsheets Page](https://www.sbimf.com/factsheets).

---

## Notes on Accuracy

- All factual responses are derived from verified HTML factsheets stored in `backend/data/raw/`.
- Citations are pulled from the `source_url` metadata field set at ingestion time.
- The retrieval uses FAISS vector similarity search with BAAI/bge-small-en-v1.5 embeddings, returning the top 3 relevant chunks.
- LLM generation uses Groq's LLaMA-3.3-70b model with a strict system prompt enforcing a 3-sentence factual limit.
