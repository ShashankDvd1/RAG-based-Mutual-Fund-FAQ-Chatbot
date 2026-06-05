# SBI Mutual Fund — Scoped Schemes Catalog

This catalog outlines the 6 selected schemes from SBI Mutual Fund, which will form the knowledge base for our facts-only RAG chatbot on the INDMoney UI interface. Selecting a scheme in the UI will filter the retrieval to these specific datasets.

| # | Scheme Name | Asset Class | Riskometer | Benchmark Index | Lock-in Period | Min SIP (₹) | Key Focus Areas / Facts | Source URL |
|---|---|---|---|---|---|---|---|---|
| **1** | **SBI Bluechip Fund** | Equity: Large Cap | Very High | S&P BSE 100 TRI | None | 500 | Bluechip companies, exit load 1% within 1 year. | [Official Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-large-cap-fund-(formerly-known-as-sbi-bluechip-fund)-43) |
| **2** | **SBI Flexicap Fund** | Equity: Flexi Cap | Very High | NIFTY 500 TRI | None | 500 | Dynamic equity allocation, exit load 1% within 1 year. | [Official Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-flexicap-fund-39) |
| **3** | **SBI Long Term Equity Fund** | Equity: ELSS | Very High | S&P BSE 500 TRI | 3 Years | 500 | Tax saving (Sec 80C), zero exit load. | [Official Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-elss-tax-saver-fund-(formerly-known-as-sbi-long-term-equity-fund)-3) |
| **4** | **SBI Small Cap Fund** | Equity: Small Cap | Very High | NIFTY Smallcap 250 TRI | None | 500 | High-growth small caps, exit load 1% within 1 year. | [Official Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-small-cap-fund-329) |
| **5** | **SBI Contra Fund** | Equity: Contra | Very High | S&P BSE 500 TRI | None | 500 | Contrarian investment strategy, exit load 1% within 1 year (no load for first 10% redeemed). | [Official Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-contra-fund-12) |
| **6** | **SBI Liquid Fund** | Debt: Liquid | Moderate | NIFTY Liquid Index A-I | None | 500 | Short-term safety, exit load scaling down from 0.0070% (Day 1) to 0.0000% (Day 7+). | [Official Factsheet](https://www.sbimf.com/sbimf-scheme-details/sbi-liquid-fund-19) |

---

## Technical metadata representation
In our FAISS vector database, every text chunk processed from these schemes will contain a `scheme` metadata tag corresponding to the Scheme Names above. 

When the user queries the API `POST /api/chat`:
1. The frontend passes the selected scheme, e.g., `"scheme": "SBI Bluechip Fund"`.
2. The backend filters vector store searches by checking `metadata["scheme_name"] == request.scheme`.
3. This eliminates cross-scheme context leakage, guaranteeing 100% accurate factual retrieval.
