### **README.md**
````markdown
# QueryFox 🦊

Simple RAG System with Agentic Routing

## Features
- 📄 Single document upload (PDF, DOCX, TXT, CSV)
- 🌐 Website scraping (1-5 pages)
- 🤖 Intelligent routing (RAG vs Web Search)
- 💬 In-memory chat (no persistence)
- 🔍 Structured content extraction
- K=3 retrieval chunks

## Quick Start
```bash
# Setup
cp .env.example .env
# Add your API keys to .env

# Run
docker-compose up --build

# Access
Frontend: http://localhost:8501
Backend API: http://localhost:8000/docs
```

## Tech Stack
- Backend: FastAPI + LangChain + LangGraph
- Frontend: Streamlit
- No Database (Stateless)
````

---

## 🚀 **HOW TO RUN**
````bash
# 1. Clone and setup
cd QueryFox
cp .env.example .env
# Edit .env and add your API keys

# 2. Start
docker-compose up --build

# 3. Open browser
http://localhost:8501
````

---

## ✅ **FEATURES**

✅ **FastAPI Backend** - RESTful API  
✅ **Streamlit Frontend** - Beautiful UI  
✅ **No Database** - Stateless, in-memory only  
✅ **Single Document** - One file OR one URL  
✅ **Structured Scraping** - Headings + Paragraphs + Lists  
✅ **K=3** - Fixed retrieval  
✅ **Chat History** - Until refresh  
✅ **Docker Ready** - Easy deployment  
✅ **Simple & Clean** - ~800 lines total  

---

