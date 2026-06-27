import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from pydantic import SecretStr
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="Resume PDF Analysis using RAG",
    page_icon="📘",
    layout="wide"
)

# ---------------------------------------------------------
# Custom CSS for Beautiful UI
# ---------------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #dfe9f3 0%, #ffffff 100%);
}
.upload-box {
    padding: 30px;
    border-radius: 20px;
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.4);
    text-align: center;
}
.chat-box {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.4);
    margin-bottom: 15px;
}
.answer-box {
    padding: 20px;
    border-radius: 15px;
    background: #ffffff;
    border-left: 5px solid #4a90e2;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# API Key
# ---------------------------------------------------------
OPENAI_API_KEY = SecretStr(os.getenv("OPENAI_API_KEY") or "")
if not OPENAI_API_KEY:
    st.error("❌ OPENAI_API_KEY not found in environment variables.")
    st.stop()

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------
st.markdown("<h1 style='text-align:center;'>📘 Resume(PDF) Analyser</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Upload your Resume(PDF) → It gets indexed → Ask questions grounded in its content</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None

# ---------------------------------------------------------
# Build Vectorstore
# ---------------------------------------------------------
def build_vectorstore_from_pdf(file):
    temp_path = "uploaded.pdf"
    with open(temp_path, "wb") as f:
        f.write(file.read())

    loader = PyPDFLoader(temp_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    return vectorstore

# ---------------------------------------------------------
# PDF Upload UI
# ---------------------------------------------------------
st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📤 Upload your Resume", type=["pdf"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file and st.session_state.vectorstore is None:
    with st.spinner("⏳ Processing PDF..."):
        st.session_state.vectorstore = build_vectorstore_from_pdf(uploaded_file)
        st.session_state.retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 5})
    st.success("✅ PDF processed! You can now ask questions.")

# ---------------------------------------------------------
# Chat Section
# ---------------------------------------------------------
if st.session_state.retriever:
    st.markdown("<h3>💬 Ask a question about the Resume</h3>", unsafe_allow_html=True)

    user_query = st.text_input("Type your question here")

    if user_query:
        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-4o-mini",
            temperature=0
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=st.session_state.retriever,
            chain_type="stuff",
            return_source_documents=True
        )

        with st.spinner("🤔 Thinking..."):
            result = qa({"query": user_query})

        st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
        st.markdown("### 📌 Answer")
        st.write(result["result"])
        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("🔍 Retrieved Context"):
            for i, doc in enumerate(result["source_documents"], 1):
                st.markdown(f"**Chunk {i} — Page {doc.metadata.get('page', 'N/A')}**")
                st.write(doc.page_content)
                st.markdown("---")
else:
    st.info("📄 Upload a Resume in PDF format to begin.")
