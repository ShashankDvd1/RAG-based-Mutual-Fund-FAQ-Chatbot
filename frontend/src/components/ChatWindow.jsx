"use client";

import React, { useEffect, useRef } from "react";

export default function ChatWindow({ messages, isLoading, activeScheme }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Helper to format basic markdown to HTML safely
  const formatMessageText = (text) => {
    if (!text) return "";

    // Escape basic HTML tags to prevent XSS (but allow our own injected tags)
    let escaped = text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    // Replace markdown links: [Anchor](URL)
    escaped = escaped.replace(
      /\[([^\]]+)\]\((https?:\/\/[^\s\)]+)\)/g,
      '<a class="chat-link" href="$2" target="_blank" rel="noopener noreferrer">$1</a>'
    );

    // Replace bold: **text**
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

    // Replace italic: *text*
    escaped = escaped.replace(/\*([^*]+)\*/g, "<em>$1</em>");

    // Replace bullet points at the beginning of a line or after a line break
    escaped = escaped.replace(/(?:^|<br\s*\/?>)\s*[\*\-]\s+/g, "<br />• ");

    // Replace newlines with breaks
    escaped = escaped.replace(/\n/g, "<br />");

    return escaped;
  };

  return (
    <div className="chat-window-container">
      {messages.length === 0 ? (
        <div className="chat-empty-state">
          <div className="empty-state-logo">
            <div className="logo-sparkle"></div>
          </div>
          <h2>SBI Mutual Fund Assistant</h2>
          <p className="empty-subtitle">
            Currently scoped to: <strong>{activeScheme.name}</strong>
          </p>
          <p className="empty-instructions">
            Ask specific factual questions about investment guidelines, exit loads, minimum investments, fund managers, and scheme rules.
          </p>
          <div className="empty-warnings border-warning">
            <span className="warning-icon">⚠</span>
            <span>
              This assistant enforces facts-only guardrails. Queries asking for investment advice, returns performance, or containing personal identification numbers (PAN, Aadhaar) will be refused automatically.
            </span>
          </div>
        </div>
      ) : (
        <div className="chat-messages-list">
          {messages.map((msg, index) => {
            const isBot = msg.sender === "bot";
            return (
              <div
                key={index}
                className={`message-row ${isBot ? "bot-row" : "user-row"}`}
              >
                {!isBot && (
                  <div className="message-bubble user-bubble">
                    <div className="message-text">{msg.text}</div>
                  </div>
                )}

                {isBot && (
                  <div className="message-bubble bot-bubble glassmorphism">
                    <div className="bot-bubble-meta">
                      <span className="bot-name">SBI MF Assistant</span>
                      {activeScheme && activeScheme.id !== "General" && (
                        <span className="scheme-tag-inline">{activeScheme.name}</span>
                      )}
                    </div>
                    
                    <div
                      className="message-text"
                      dangerouslySetInnerHTML={{
                        __html: formatMessageText(msg.text),
                      }}
                    />

                    {/* Citations / Sources */}
                    {msg.retrieved_chunks && msg.retrieved_chunks.length > 0 && (
                      <div className="citations-container">
                        <div className="citations-header">
                          <svg
                            viewBox="0 0 24 24"
                            width="14"
                            height="14"
                            stroke="currentColor"
                            strokeWidth="2"
                            fill="none"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          >
                            <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                            <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
                          </svg>
                          <span>Sources & Citations</span>
                        </div>
                        <div className="citations-grid">
                          {msg.retrieved_chunks.map((chunk, cIdx) => (
                            <a
                              key={cIdx}
                              href={chunk.source_url || "https://www.sbimf.com"}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="citation-pill"
                            >
                              <div className="citation-pill-title">
                                {chunk.title || chunk.scheme_name || "Factsheet"}
                              </div>
                              <div className="citation-pill-footer">
                                <span className="citation-date">As on: {chunk.date_accessed}</span>
                                <span className="citation-link-icon">↗</span>
                              </div>
                            </a>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}

          {isLoading && (
            <div className="message-row bot-row">
              <div className="message-bubble bot-bubble glassmorphism typing-bubble">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      )}
    </div>
  );
}
