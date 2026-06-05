# RAG-based Mutual Fund FAQ Chatbot — Problem Statement

## Submission Deadline

**June 5, 11:59:00 PM (Asia/Calcutta)**

---

## Product Selection

Pick **ONE** product from the following list (the same product will be used for the next LIP challenge):

- INDMoney
- Groww
- PowerUp Money
- Wealth Monitor
- Kuvera

---

## Milestone Brief — Mutual Fund FAQs (Facts-Only Q&A)

Build a small FAQ assistant that answers **facts** about mutual fund schemes — e.g., expense ratio, exit load, minimum SIP, lock-in (ELSS), riskometer, benchmark, and how to download statements — using **only official public pages**. Every answer must include **one source link**. No advice.

---

## Who This Helps

- Retail users comparing schemes.
- Support / content teams answering repetitive MF questions.

---

## What You Must Build

### 1. Scope Your Corpus

- Pick **one AMC** and **3–5 schemes** under it (e.g., one large-cap, one flexi-cap, one ELSS).
- Collect **15–25 public pages** from AMC / SEBI / AMFI:
  - Factsheets
  - KIM / SID
  - Scheme FAQs
  - Fee / charges pages
  - Riskometer / benchmark notes
  - Statement / tax-doc guides

### 2. FAQ Assistant (Working Prototype)

The assistant must:

- Answer **factual queries only**, such as:
  - *"Expense ratio of \<scheme\>?"*
  - *"ELSS lock-in?"*
  - *"Minimum SIP?"*
  - *"Exit load?"*
  - *"Riskometer / benchmark?"*
  - *"How to download capital-gains statement?"*
- Show **one clear citation link** in every answer.
- **Refuse** opinionated / portfolio questions (e.g., *"Should I buy/sell?"*) with a polite, facts-only message and a relevant educational link.

### 3. Tiny UI

- Welcome line
- 3 example questions
- A note: **"Facts-only. No investment advice."**

---

## Key Constraints

| Constraint | Details |
|---|---|
| **Public sources only** | No screenshots of the app back-end; no third-party blogs as sources. |
| **No PII** | Do not accept/store PAN, Aadhaar, account numbers, OTPs, emails, or phone numbers. |
| **No performance claims** | Don't compute/compare returns; link to the official factsheet if asked. |
| **Clarity & transparency** | Keep answers ≤ 3 sentences; add *"Last updated from sources: \<date\>"*. |

---

## Deliverables

| # | Deliverable | Description |
|---|---|---|
| 1 | **Working prototype link** | App / notebook, or a ≤ 3-min demo video if hosting isn't possible. |
| 2 | **Source list** | CSV / MD of the 15–25 URLs used. |
| 3 | **README** | Setup steps, scope (AMC + schemes), and known limits. |
| 4 | **Sample Q&A file** | 5–10 queries with the assistant's answers + links. |
| 5 | **Disclaimer snippet** | The facts-only / no-advice disclaimer used in the UI. |
