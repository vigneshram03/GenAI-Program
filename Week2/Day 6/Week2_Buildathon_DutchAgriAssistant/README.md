# 🌿 Dutch Agri Assistant

An AI-powered RAG chatbot built with **Streamlit**, **LangChain**, **OpenAI**, **FAISS**, and **BeautifulSoup**.

## Features

- Crawl Government of the Netherlands Agriculture websites
- Breadth-First Search (BFS) crawler
- BeautifulSoup content extraction
- Recursive text chunking
- OpenAI embeddings (`text-embedding-3-small`)
- FAISS vector search
- GPT-4o-mini question answering
- Streaming responses
- LangSmith tracing
- Source citations
- Persistent FAISS cache

## Architecture

Website
→ BeautifulSoup Scraper
→ BFS Crawler
→ LangChain Documents
→ Text Splitter
→ OpenAI Embeddings
→ FAISS
→ Similarity Retriever
→ GPT-4o-mini
→ Streamlit UI

## Project Structure

```
DutchAgriAssistant/
│
├── app.py
├── ragengine.py
├── crawler.py
├── scraper.py
├── requirements.txt
├── .env.example
├── README.md
└── faiss_index/
```

## Installation

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Environment

Copy `.env.example` to `.env` and add your API keys.

## Run

```bash
streamlit run app.py
```

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenAI
- FAISS
- BeautifulSoup
- LangSmith

## License

MIT