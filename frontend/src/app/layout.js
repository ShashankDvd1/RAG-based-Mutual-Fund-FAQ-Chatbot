import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Analytics } from "@vercel/analytics/react";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "SBI Mutual Fund FAQ Chatbot | RAG-Powered Facts Assistant",
  description:
    "A facts-only AI assistant for SBI Mutual Fund scheme inquiries. Powered by RAG (Retrieval-Augmented Generation) with FAISS vector search and Groq LLaMA. Get instant factual answers about fund rules, exit loads, and investment guidelines.",
  keywords: [
    "SBI Mutual Fund",
    "FAQ chatbot",
    "RAG chatbot",
    "mutual fund assistant",
    "FAISS",
    "Groq LLaMA",
    "SBI Bluechip",
    "SBI Liquid Fund",
    "SBI Small Cap",
    "investment FAQ",
  ],
  openGraph: {
    title: "SBI Mutual Fund FAQ Chatbot",
    description:
      "Facts-only AI assistant for SBI Mutual Fund scheme inquiries. No investment advice — only verified factsheet data.",
    type: "website",
  },
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
