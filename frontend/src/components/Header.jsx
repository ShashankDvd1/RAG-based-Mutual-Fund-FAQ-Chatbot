"use client";

import React from "react";

export default function Header({ status = "connected" }) {
  return (
    <header className="app-header glassmorphism">
      <div className="header-left">
        <div className="logo-icon">
          <div className="logo-inner"></div>
        </div>
        <div className="header-titles">
          <h1 className="header-title gradient-text">SBI Mutual Fund FAQ</h1>
          <span className="header-tag">RAG Chatbot</span>
        </div>
      </div>
      <div className="header-right">
        <div className={`status-indicator ${status}`}>
          <span className="status-dot"></span>
          <span className="status-text">{status === "connected" ? "API Online" : "Connecting..."}</span>
        </div>
      </div>
    </header>
  );
}
