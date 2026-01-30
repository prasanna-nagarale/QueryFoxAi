import streamlit as st
import requests
import json

API_URL = "http://backend:8000"

st.set_page_config(page_title="QueryFox", page_icon="🦊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.main-header { font-size: 3rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.5rem; }
.subtitle { text-align: center; color: #6b7280; font-size: 1.2rem; margin-bottom: 2rem; }
.stButton > button { border-radius: 10px; padding: 0.75rem 2rem; font-weight: 600; transition: all 0.3s; width: 100%; }
.stTextInput > div > div > input { border-radius: 10px; }
.stFileUploader { border: 2px dashed #667eea; border-radius: 15px; padding: 2rem; background: linear-gradient(135deg, #667eea08 0%, #764ba208 100%); }
div[data-testid="stMetricValue"] { font-size: 2rem; font-weight: 700; color: #667eea; }
</style>
""", unsafe_allow_html=True)

if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'num_chunks' not in st.session_state:
    st.session_state.num_chunks = 0
if 'source_name' not in st.session_state:
    st.session_state.source_name = ""

st.markdown('<h1 class="main-header">🦊 QueryFox</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Advanced RAG System with Intelligent Routing</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📄 Documents", "1" if st.session_state.data_loaded else "0")
with col2:
    st.metric("🧩 Chunks", st.session_state.num_chunks)
with col3:
    st.metric("💬 Messages", len(st.session_state.chat_history))

st.divider()

if not st.session_state.data_loaded:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Upload Document")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx", "csv"], key="file_uploader")
        
        if st.button("🔄 Process File", key="process_file", disabled=not uploaded_file):
            with st.spinner("Processing file..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{API_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.vectorstore = data["vectorstore_data"]
                        st.session_state.num_chunks = data["num_chunks"]
                        st.session_state.source_name = uploaded_file.name
                        st.session_state.data_loaded = True
                        st.success(data["message"])
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("### 🌐 Scrape Website")
        url = st.text_input("Enter URL", placeholder="https://example.com")
        max_pages = st.slider("Max Pages", 1, 5, 1)
        
        if st.button("🔍 Scrape", key="scrape_button", disabled=not url):
            with st.spinner("Scraping website..."):
                try:
                    response = requests.post(f"{API_URL}/scrape", json={"url": url, "max_pages": max_pages})
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.vectorstore = data["vectorstore_data"]
                        st.session_state.num_chunks = data["num_chunks"]
                        st.session_state.source_name = url
                        st.session_state.data_loaded = True
                        st.success(f"{data['message']} - {data['pages_scraped']} pages")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

else:
    st.info(f"📌 Data Source: **{st.session_state.source_name}**")
    
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📚 Sources"):
                    for i, src in enumerate(msg["sources"], 1):
                        st.markdown(f"**Source {i}:**")
                        st.text(src["content"])
    
    if user_query := st.chat_input("💭 Ask anything..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        with st.chat_message("user"):
            st.markdown(user_query)
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/query",
                        json={"query": user_query, "vectorstore_data": st.session_state.vectorstore}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.markdown(data["answer"])
                        
                        if data.get("sources"):
                            with st.expander("📚 Sources"):
                                for i, src in enumerate(data["sources"], 1):
                                    st.markdown(f"**Source {i}:**")
                                    st.text(src["content"])
                        
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": data["answer"],
                            "sources": data.get("sources")
                        })
                    else:
                        error_msg = f"❌ Error: {response.json().get('detail', 'Unknown error')}"
                        st.error(error_msg)
                        st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    col1, col2 = st.columns([1, 1])
    if col1.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()
    if col2.button("🔄Reset All"):
        st.session_state.vectorstore = None
        st.session_state.chat_history = []
        st.session_state.data_loaded = False
        st.session_state.num_chunks = 0
        st.session_state.source_name = ""
        st.rerun()
        st.divider()
        st.caption("💡 Powered by FastAPI • LangGraph • Groq • Tavily • FAISS")