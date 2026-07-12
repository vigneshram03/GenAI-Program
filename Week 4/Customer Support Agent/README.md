\# 🤖 Multi-Agent Customer Support System with FAISS RAG \& Live Web Search



An advanced, production-ready multi-agent customer support workspace built using the \*\*CrewAI\*\* orchestration framework and a custom \*\*LangChain + FAISS Retrieval-Augmented Generation (RAG)\*\* pipeline. The system features a modern, colorful \*\*Streamlit\*\* user interface designed for seamless real-time support analysis.



\---



\## 📌 Project Overview

\[cite\_start]This application orchestrates three specialized AI agents working sequentially to resolve customer queries efficiently\[cite: 6, 7]:



1\. \*\*Internal FAQ Assistant (RAG Agent):\*\* Semantically searches an internal proprietary text database (`knowledge\_base.txt`) via a FAISS vector store to fetch exact company policies and guidelines.

2\. \*\*Web Search Assistant:\*\* Complements internal documentation by searching the live web for external context, recent industry updates, or standard authentication practices.

3\. \[cite\_start]\*\*Entry Agent:\*\* Automatically compiles the original user query alongside both generated responses, formats the data, and writes the log history to a local text file (`answers.txt`)\[cite: 72].



\---



\## 🚀 System Architecture \& Flow



\* \*\*User Input:\*\* Enter any customer ticket or query into the Streamlit portal.

\* \*\*Vector Execution:\*\* LangChain reads your knowledge base, splits text into overlapping chunks, creates semantic embeddings via OpenAI, and caches it in a high-speed memory-mapped FAISS index.

\* \[cite\_start]\*\*Sequential Crew Optimization:\*\* The information flows step-by-step through the CrewAI pipeline, passing context from one agent to the next\[cite: 14, 22].

\* \*\*Output Presentation:\*\* The user interface dynamically loads matching emerald and royal blue markdown panels showcasing split internal vs. external data insights.



\---



\## ⚙️ Step-by-Step Local Setup



Follow these precise steps to spin up the support engine environment on your local machine:



\### 1. Clone \& Navigate to Project Directory

```bash

git clone https://github.com/vigneshram03/GenAI-Program/tree/main/Week%204/Customer%20Support%20Agent

cd Customer Support Agent

