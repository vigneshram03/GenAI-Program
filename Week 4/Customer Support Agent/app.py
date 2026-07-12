import os
import streamlit as st
# pyrefly: ignore [missing-import]
from crew_logic import run_support_crew

# ---------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Support Ecosystem Portal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS injection for smooth transitions, vibrant card containers, and sleek borders
st.markdown("""
    <style>
    /* Global App Background and Theme colors */
    .stApp { background-color: #fafbfc; }
    
    /* Header Typography styling */
    .main-header { font-size: 2.8rem; font-weight: 800; color: #1E293B; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.1rem; color: #64748B; margin-bottom: 2rem; }
    
    /* Input Container & Buttons customization */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25);
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(79, 70, 229, 0.4);
    }
    
    /* Custom CSS Cards for Agent Windows */
    .result-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-top: 15px;
        border: 1px solid #E2E8F0;
        transition: transform 0.2s ease;
    }
    .result-card:hover { transform: translateY(-3px); }
    
    .card-internal { border-top: 5px solid #10B981; } /* Emerald Green */
    .card-external { border-top: 5px solid #3B82F6; } /* Royal Blue */
    
    .card-title { font-size: 1.25rem; font-weight: 700; color: #1E293B; margin-bottom: 12px; display: flex; align-items: center; }
    .card-body { color: #334155; font-size: 0.95rem; line-height: 1.6; }
    
    /* Sidebar styling adjustments */
    section[data-testid="stSidebar"] { background-color: #0F172A; color: #F8FAFC; }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p { color: #F8FAFC !important; }
    .status-badge { padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; float: right; }
    .badge-active { background-color: #064E3B; color: #34D399; }
    .badge-missing { background-color: #7F1D1D; color: #F87171; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# SIDEBAR SYSTEM CONTROLS
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='margin-top:10px;'>⚙️ System Diagnostics</h2>", unsafe_allow_html=True)
    st.markdown("Monitor connection states and agent knowledge availability below.")
    st.markdown("---")
    
    openai_ready = "OPENAI_API_KEY" in os.environ
    serper_ready = "SERPER_API_KEY" in os.environ
    file_ready = os.path.exists("knowledge_base.txt")
    
    # Dynamic badges mapped using custom HTML rules defined above
    def get_badge(status):
        return f'<span class="status-badge badge-active">Active</span>' if status else f'<span class="status-badge badge-missing">Missing</span>'

    st.markdown(f"🧠 OpenAI Core: {get_badge(openai_ready)}", unsafe_allow_html=True)
    st.markdown(f"🌐 Web Search Engine: {get_badge(serper_ready)}", unsafe_allow_html=True)
    st.markdown(f"📄 KB Text Index: {get_badge(file_ready)}", unsafe_allow_html=True)
    
    st.markdown("<br><br><hr><p style='font-size: 0.8rem; color: #94A3B8;'>Enterprise Orchestration Engine v2.1.0</p>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# MAIN APPLICATION INTERFACE
# ---------------------------------------------------------------------------
st.markdown("<div class='main-header'>🤖 AI Customer Support Agent</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>A seamless multi-agent workspace bridging local vector datasets with live search environments.</div>", unsafe_allow_html=True)

# User Query Workspace Area
user_query = st.text_input(
    "What customer query can the crew assist you with today?",
    placeholder="e.g., When is the corporate salary cut off date of each month?",
    key="dashboard_query"
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 Invoke Support Crew") and user_query:
    if not (openai_ready and serper_ready):
        st.error("Execution blocked: Ensure your API environment tokens are fully active in your execution context.")
    elif not file_ready:
        st.error("Execution blocked: 'knowledge_base.txt' was not verified inside your active path directory.")
    else:
        # High fidelity processing feedback
        with st.status("⚡ Initializing Multi-Agent System Processes...", expanded=True) as status:
            st.write("🔍 Extracting vector indices via local FAISS pipeline...")
            st.write("📡 Spin-up: Internal FAQ Assistant & Live Web Researcher active.")
            
            # Fire backend logic execution 
            internal_ans, external_ans = run_support_crew(user_query)
            
            status.update(label="✅ Processing complete! Rendering response panels...", state="complete", expanded=False)
        
        # Output Presentation Section Layout
        st.markdown("### 📋 Formulated Agent Analysis")
        
        # Dual panel split system
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown(f"""
                <div class="result-card card-internal">
                    <div class="card-title">📁 🌟 Answer 1: Company Knowledge Base (RAG)</div>
                    <div class="card-body">{internal_ans}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div class="result-card card-external">
                    <div class="card-title">🌐 🔍 Answer 2: Live External Web Context</div>
                    <div class="card-body">{external_ans}</div>
                </div>
            """, unsafe_allow_html=True)

        st.toast("System logs saved directly to answers.txt!", icon="💾")