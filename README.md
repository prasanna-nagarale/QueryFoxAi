# QueryFox 🦊

**Advanced RAG System with Intelligent Agentic Routing**

A production-ready document intelligence system that combines Retrieval Augmented Generation (RAG) with intelligent query routing. Built with FastAPI and Streamlit, featuring automatic decision-making between local document search and real-time web search.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- 🤖 **Intelligent Query Routing** - Automatically routes between document RAG and web search using LangGraph
- 📄 **Multi-Format Support** - PDF, DOCX, TXT, CSV document processing
- 🌐 **Smart Web Scraping** - Structured content extraction (headings, paragraphs, lists) with recursive crawling
- 🔍 **Semantic Search** - FAISS vector database with K=3 retrieval optimization
- ⚡ **Fast Inference** - Groq API (Llama 3.3 70B) for <2s response times
- 💬 **Interactive Chat** - Real-time Streamlit interface with source attribution
- 🐳 **Docker Ready** - Containerized deployment with Docker Compose

---

## 🏗️ Architecture
```
┌──────────────┐      ┌─────────────────┐      ┌──────────────┐
│   Streamlit  │ ───► │  FastAPI + RAG  │ ───► │  Groq LLM    │
│   Frontend   │      │  + LangGraph    │      │  (Llama 3.3) │
└──────────────┘      └─────────────────┘      └──────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              ┌──────────┐        ┌──────────┐
              │  FAISS   │        │  Tavily  │
              │  Vector  │        │  Web     │
              │  Search  │        │  Search  │
              └──────────┘        └──────────┘
```

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI - High-performance async API
- LangChain & LangGraph - AI orchestration & agentic routing
- FAISS - Vector similarity search
- Groq API - Fast LLM inference
- Tavily API - Real-time web search

**Frontend:**
- Streamlit - Interactive web UI

**AI/ML:**
- HuggingFace Transformers (all-MiniLM-L6-v2)
- PyPDF, python-docx - Document processing
- BeautifulSoup4 - Web scraping

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)
- Groq API Key ([Get here](https://console.groq.com))
- Tavily API Key ([Get here](https://tavily.com))

### Local Setup (Recommended for Development)
```bash
# 1. Clone repository
git clone https://github.com/prasanna-nagarale/QueryFoxAi.git
cd QueryFox

# 2. Create environment file
cp .env.example .env
# Add your API keys to .env

# 3. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 4. Start backend (Terminal 1)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 5. Frontend setup (Terminal 2)
cd ../frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Start frontend
streamlit run app.py
```

**Access:** http://localhost:8501

---

### Docker Setup (Recommended for Production)
```bash
# 1. Clone and configure
git clone https://github.com/prasanna-nagarale/QueryFoxAi.git
cd QueryFox
cp .env.example .env
# Add your API keys to .env

# 2. Start with Docker
docker-compose up --build

# Access:
# Frontend: http://localhost:8501
# Backend API: http://localhost:8000/docs
```

---

## 📝 Environment Variables

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

---

## 💻 Usage

### 1. Upload Document
- Click "Upload Document"
- Select PDF, DOCX, TXT, or CSV file
- System processes and creates embeddings

### 2. Scrape Website
- Enter URL in "Scrape Website"
- Set max pages (1-5)
- System extracts structured content

### 3. Ask Questions
- Type your question in chat
- System automatically routes to RAG or web search
- Receive answer with source attribution

---

## 📊 Performance

- **Response Time:** <2 seconds (RAG mode)
- **Document Processing:** 3-7 seconds (average)
- **Retrieval Accuracy:** K=3 optimized chunks
- **Supported File Size:** Up to 10MB
- **Web Scraping:** 1-5 pages with structured extraction

---

## 🎯 How It Works

1. **Query Analysis** - LangGraph analyzes if query needs current info or can use documents
2. **Intelligent Routing:**
   - **RAG Path:** Semantic search in FAISS → Retrieve K=3 chunks → Generate answer
   - **Web Path:** Tavily search → Fetch articles → Synthesize answer
3. **Response Generation** - Groq LLM creates contextual answer with sources

---

## 📂 Project Structure
```
QueryFox/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── core/
│   │   │   ├── rag_engine.py    # RAG logic
│   │   │   ├── langgraph_agent.py  # Agentic routing
│   │   │   ├── document_processor.py
│   │   │   ├── web_scraper.py
│   │   │   └── embeddings.py
│   │   └── models/
│   │       └── schemas.py       # Pydantic models
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py                   # Streamlit UI
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/upload` | POST | Upload and process document |
| `/scrape` | POST | Scrape and process website |
| `/query` | POST | Query with intelligent routing |
| `/docs` | GET | Interactive API documentation |

**Full API Docs:** http://localhost:8000/docs (when running)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) - AI orchestration framework
- [Groq](https://groq.com) - Fast LLM inference
- [Tavily](https://tavily.com) - Web search API
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search
- [Streamlit](https://streamlit.io) - UI framework

---

## 📧 Contact

**Prasanna Nagarale**
- Email: nagaraleprasanna@gmail.com
- LinkedIn: [linkedin.com/in/prasanna-ai](https://linkedin.com/in/prasanna-ai)
- GitHub: [github.com/prasanna-nagarale](https://github.com/prasanna-nagarale)
- Portfolio: [prasanna-nagarale.github.io/prasanna-portfolio](https://prasanna-nagarale.github.io/prasanna-portfolio)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

**Built with ❤️ using FastAPI, LangGraph, and Groq**
