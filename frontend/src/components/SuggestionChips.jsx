"use client";

import React from "react";

const CHIPS_BY_SCHEME = {
  "General": [
    "How can I check my mutual fund statement?",
    "What is the exit load on SBI funds?",
    "How to update email/mobile number?"
  ],
  "SBI Bluechip Fund": [
    "What is the exit load for SBI Bluechip Fund?",
    "What is the minimum investment amount?",
    "Show key ratios of SBI Bluechip Fund."
  ],
  "SBI Long Term Equity Fund": [
    "Is there a lock-in period for SBI Long Term Equity Fund?",
    "What is the tax deduction limit under 80C?",
    "Who is the fund manager for SBI Long Term Equity Fund?"
  ],
  "SBI Flexicap Fund": [
    "What is the asset allocation of SBI Flexicap Fund?",
    "What is the minimum SIP amount?",
    "Who is the fund manager?"
  ],
  "SBI Contra Fund": [
    "What is the investment strategy of SBI Contra Fund?",
    "What is the exit load for Contra Fund?",
    "Show the expense ratio."
  ],
  "SBI Liquid Fund": [
    "What is the exit load for SBI Liquid Fund?",
    "What is the maturity profile of SBI Liquid Fund?",
    "What is the minimum investment for SBI Liquid Fund?"
  ],
  "SBI Small Cap Fund": [
    "What is the exit load for SBI Small Cap Fund?",
    "What is the minimum top-up amount?",
    "Show the riskometer status of SBI Small Cap Fund."
  ]
};

export default function SuggestionChips({ schemeId, onSelectQuery, disabled }) {
  const chips = CHIPS_BY_SCHEME[schemeId] || CHIPS_BY_SCHEME["General"];

  return (
    <div className="suggestion-chips-container">
      <span className="chips-label">Suggestions:</span>
      <div className="chips-wrapper">
        {chips.map((query, index) => (
          <button
            key={index}
            className="suggestion-chip"
            onClick={() => !disabled && onSelectQuery(query)}
            disabled={disabled}
            title={query}
          >
            {query}
          </button>
        ))}
      </div>
    </div>
  );
}
