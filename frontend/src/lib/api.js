const API_URL = process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === "production" ? "https://rag-based-mutual-fund-faq-chatbot-ch45.onrender.com" : "http://127.0.0.1:8000");

/**
 * Sends a query to the FastAPI RAG backend.
 * 
 * @param {string} question The user question.
 * @param {string|null} scheme The scheme identifier/name context.
 * @returns {Promise<{answer: string, retrieved_chunks: Array}>}
 */
export async function queryChatbot(question, scheme = null) {
  try {
    const url = `${API_URL}/api/chat`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        scheme: scheme && scheme !== "General" ? scheme : null,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      let errorJson;
      try {
        errorJson = JSON.parse(errorText);
      } catch (e) {
        // Not JSON
      }
      const message = errorJson?.detail || `API error (${response.status})`;
      throw new Error(message);
    }

    return await response.json();
  } catch (error) {
    console.error("Error calling chatbot API:", error);
    throw error;
  }
}

/**
 * Checks the health status of the backend API.
 * 
 * @returns {Promise<boolean>} True if online, false otherwise.
 */
export async function checkApiHealth() {
  try {
    const response = await fetch(`${API_URL}/health`, {
      method: "GET",
      // Set short timeout
      signal: AbortSignal.timeout(5000)
    });
    return response.ok;
  } catch (error) {
    console.warn("Backend API health check failed:", error);
    return false;
  }
}
