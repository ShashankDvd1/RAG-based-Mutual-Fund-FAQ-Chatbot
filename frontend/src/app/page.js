"use client";

import { useState, useEffect, useCallback } from "react";
import Header from "@/components/Header";
import DisclaimerBanner from "@/components/DisclaimerBanner";
import SchemeSelector, { SCHEMES } from "@/components/SchemeSelector";
import SuggestionChips from "@/components/SuggestionChips";
import ChatWindow from "@/components/ChatWindow";
import InputBar from "@/components/InputBar";
import { queryChatbot, checkApiHealth } from "@/lib/api";

const DEFAULT_SCHEME = SCHEMES[0]; // "General / All Schemes"

export default function Home() {
  const [selectedScheme, setSelectedScheme] = useState(DEFAULT_SCHEME);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState("connecting");

  // Check API health on mount
  useEffect(() => {
    const pingHealth = async () => {
      const isOnline = await checkApiHealth();
      setApiStatus(isOnline ? "connected" : "connecting");
    };
    pingHealth();
  }, []);

  // Handle scheme selection — also clears chat context
  const handleSelectScheme = useCallback((scheme) => {
    setSelectedScheme(scheme);
    setMessages([]);
  }, []);

  // Core message send handler
  const handleSendMessage = useCallback(
    async (question) => {
      if (!question.trim() || isLoading) return;

      const userMessage = {
        sender: "user",
        text: question,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);

      try {
        const data = await queryChatbot(
          question,
          selectedScheme.id === "General" ? null : selectedScheme.id
        );

        const botMessage = {
          sender: "bot",
          text: data.answer,
          retrieved_chunks: data.retrieved_chunks || [],
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        const errorMessage = {
          sender: "bot",
          text: `⚠️ **Connection Error:** Could not reach the backend API.\n\n${error.message}\n\nPlease check your deployment configuration or ensure the backend server is running.`,
          retrieved_chunks: [],
          timestamp: new Date().toISOString(),
          isError: true,
        };
        setMessages((prev) => [...prev, errorMessage]);
        setApiStatus("connecting");
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, selectedScheme]
  );

  // Allow suggestion chips to trigger send
  const handleChipSelect = useCallback(
    (query) => {
      if (!isLoading) handleSendMessage(query);
    },
    [isLoading, handleSendMessage]
  );

  return (
    <div className="app-container">
      {/* Disclaimer bar at top */}
      <DisclaimerBanner />

      {/* App header */}
      <Header status={apiStatus} />

      {/* Main body: sidebar + chat */}
      <div className="main-layout">
        {/* Left sidebar: Scheme selector */}
        <aside className="sidebar-panel">
          <SchemeSelector
            selectedScheme={selectedScheme}
            onSelectScheme={handleSelectScheme}
          />
        </aside>

        {/* Right: Chat panel */}
        <main className="chat-panel">
          {/* Scrollable messages area */}
          <ChatWindow
            messages={messages}
            isLoading={isLoading}
            activeScheme={selectedScheme}
          />

          {/* Footer with chips + input */}
          <div className="chat-footer">
            <SuggestionChips
              schemeId={selectedScheme.id}
              onSelectQuery={handleChipSelect}
              disabled={isLoading}
            />
            <InputBar
              onSendMessage={handleSendMessage}
              disabled={isLoading}
              placeholder={
                selectedScheme.id === "General"
                  ? "Ask anything about SBI Mutual Funds..."
                  : `Ask about ${selectedScheme.name}...`
              }
            />
          </div>
        </main>
      </div>
    </div>
  );
}
