import time
import streamlit as st
from dotenv import load_dotenv
from crawler import WebsiteCrawler
from ragengine import RAGEngine
import os

load_dotenv()

print(os.getenv("LANGSMITH_ENDPOINT"))
print(os.getenv("LANGSMITH_PROJECT"))
print(os.getenv("LANGSMITH_API_KEY")[:10])

WEBSITE_URL = "https://www.government.nl/themes/economy/agriculture/agriculture-and-horticulture"
MAX_PAGES = 25

st.set_page_config(page_title="Dutch Agri Assistant",
                   page_icon="🌿",
                   layout="wide")

for k,v in {
    "initialized":False,
    "rag":None,
    "messages":[],
    "stats":{"pages":0,"chunks":0},
    "website_summary":""
}.items():
    st.session_state.setdefault(k,v)

st.title("🌿 Dutch Agri Assistant")
st.caption("Government of the Netherlands Agriculture")

if not st.session_state.initialized:
    progress = st.progress(0,text="Loading Dutch Agriculture Knowledge Base...")

    crawler = WebsiteCrawler(WEBSITE_URL,MAX_PAGES)
    progress.progress(20,text="Crawling website...")
    pages = crawler.crawl()

    rag = RAGEngine()
    progress.progress(60,text="Building vector database...")
    rag.index_pages(pages,WEBSITE_URL)

    progress.progress(90,text="Generating website summary...")
    try:
        summary = rag.generate_summary()
    except Exception:
        summary = ""

    st.session_state.rag = rag
    st.session_state.website_summary = summary
    st.session_state.stats = {
        "pages":len(pages),
        "chunks":len(rag.chunks)
    }
    st.session_state.initialized = True
    progress.progress(100,text="Ready")
    progress.empty()
    st.rerun()

with st.sidebar:
    st.subheader("📊 Statistics")
    c1,c2 = st.columns(2)
    c1.metric("Pages",st.session_state.stats["pages"])
    c2.metric("Chunks",st.session_state.stats["chunks"])

    st.divider()
    st.subheader("💡 Suggested Questions")
    for q in [
        "What is horticulture?",
        "What support is available for farmers?",
        "What are greenhouse crops?",
        "What is sustainable agriculture?",
        "How does the government support organic farming?"
    ]:
        if st.button(q,use_container_width=True):
            st.session_state["pending_question"] = q

with st.expander("📖 Indexed Website Summary",expanded=True):
    st.write(st.session_state.website_summary)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"]=="assistant" and msg.get("sources"):
            with st.expander("📚 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"**{s['title']}**")
                    st.caption(s["url"])

question = st.session_state.pop("pending_question",None)
typed = st.chat_input("Ask anything about Dutch Agriculture...")

if typed:
    question = typed

if question:
    st.session_state.messages.append({"role":"user","content":question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        start=time.perf_counter()
        placeholder=st.empty()
        answer=""
        for token in st.session_state.rag.stream_answer(question):
            answer += token
            placeholder.markdown(answer+"▌")
        placeholder.markdown(answer)

        sources = st.session_state.rag.get_sources(question)

        with st.expander("📚 Sources"):
            for s in sources:
                st.markdown(f"**{s['title']}**")
                st.caption(s["url"])

        elapsed=time.perf_counter()-start
        st.caption(f"Response Time: {elapsed:.2f}s")

    st.session_state.messages.append({
        "role":"assistant",
        "content":answer,
        "sources":sources
    })

    st.rerun()
