from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    vectorstore_data: Optional[str] = None

class QueryResponse(BaseModel):
    answer: str
    sources: Optional[List[Dict[str, Any]]] = None
    steps: List[str]
    needs_search: bool

class FileUploadResponse(BaseModel):
    message: str
    num_chunks: int
    vectorstore_data: str

class URLScrapeRequest(BaseModel):
    url: str = Field(..., pattern=r'^https?://')
    max_pages: int = Field(default=1, ge=1, le=5)

class URLScrapeResponse(BaseModel):
    message: str
    num_chunks: int
    vectorstore_data: str
    pages_scraped: int