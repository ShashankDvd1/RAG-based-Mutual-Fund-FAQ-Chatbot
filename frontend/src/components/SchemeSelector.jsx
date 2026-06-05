"use client";

import React from "react";

export const SCHEMES = [
  {
    id: "General",
    name: "General / All Schemes",
    category: "General FAQ & Guide",
    risk: "N/A",
    riskClass: "risk-na",
    desc: "Query general FAQs, statement instructions, and account guidelines across all funds."
  },
  {
    id: "SBI Bluechip Fund",
    name: "SBI Bluechip Fund",
    category: "Equity - Large Cap",
    risk: "Very High",
    riskClass: "risk-very-high",
    desc: "Focuses on large-cap bluechip stocks with long-term growth potential."
  },
  {
    id: "SBI Long Term Equity Fund",
    name: "SBI Long Term Equity Fund",
    category: "Equity - ELSS (Tax Saver)",
    risk: "Very High",
    riskClass: "risk-very-high",
    desc: "Equity Linked Saving Scheme offering tax benefits under Section 80C."
  },
  {
    id: "SBI Flexicap Fund",
    name: "SBI Flexicap Fund",
    category: "Equity - Flexi Cap",
    risk: "Very High",
    riskClass: "risk-very-high",
    desc: "Invests across large-cap, mid-cap, and small-cap stocks."
  },
  {
    id: "SBI Contra Fund",
    name: "SBI Contra Fund",
    category: "Equity - Contra",
    risk: "Very High",
    riskClass: "risk-very-high",
    desc: "Focuses on contrarian investment strategy, buying out-of-favor stocks."
  },
  {
    id: "SBI Liquid Fund",
    name: "SBI Liquid Fund",
    category: "Debt - Liquid",
    risk: "Low to Moderate",
    riskClass: "risk-low-moderate",
    desc: "High liquidity and lower risk by investing in short-term debt securities."
  },
  {
    id: "SBI Small Cap Fund",
    name: "SBI Small Cap Fund",
    category: "Equity - Small Cap",
    risk: "Very High",
    riskClass: "risk-very-high",
    desc: "Focuses on high-growth potential small-cap companies."
  }
];

export default function SchemeSelector({ selectedScheme, onSelectScheme }) {
  return (
    <div className="scheme-selector-container">
      <div className="sidebar-section-header">
        <h3>Select Fund Context</h3>
        <p>Your questions will be answered in the context of this fund.</p>
      </div>
      <div className="scheme-list">
        {SCHEMES.map((scheme) => {
          const isActive = selectedScheme.id === scheme.id;
          return (
            <div
              key={scheme.id}
              className={`scheme-card ${isActive ? "active" : ""}`}
              onClick={() => onSelectScheme(scheme)}
            >
              <div className="scheme-card-header">
                <span className="scheme-category">{scheme.category}</span>
                <span className={`scheme-risk-badge ${scheme.riskClass}`}>
                  {scheme.risk} Risk
                </span>
              </div>
              <h4 className="scheme-name">{scheme.name}</h4>
              <p className="scheme-desc">{scheme.desc}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
