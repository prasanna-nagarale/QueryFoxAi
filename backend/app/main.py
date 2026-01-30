from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.models.schemas import QueryRequest, QueryResponse, FileUploadResponse, URLScrapeRequest, URLScrapeResponse
from app.core.rag_engine import rag_engine
from app.core.document_processor import document_processor
from app.core.web_scraper import web_scraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="QueryFox API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "QueryFox API 🦊", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")
        
        vectorstore_data, num_chunks = await document_processor.process_file(content, file.filename)
        
        return FileUploadResponse(
            message=f"✅ {file.filename} processed successfully",
            num_chunks=num_chunks,
            vectorstore_data=vectorstore_data
        )
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/scrape", response_model=URLScrapeResponse)
async def scrape_website(request: URLScrapeRequest):
    try:
        vectorstore_data, num_chunks, pages_scraped = await web_scraper.scrape_url(request.url, request.max_pages)
        
        return URLScrapeResponse(
            message=f"✅ Scraped {pages_scraped} page(s) successfully",
            num_chunks=num_chunks,
            vectorstore_data=vectorstore_data,
            pages_scraped=pages_scraped
        )
    except Exception as e:
        logger.error(f"Scrape error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        result = await rag_engine.query(request.query, request.vectorstore_data)
        return QueryResponse(**result)
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))