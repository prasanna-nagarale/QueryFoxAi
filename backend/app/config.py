from pydantic_settings import BaseSettings
import os
from pathlib import Path

# Get the backend directory
BASE_DIR = Path(__file__).resolve().parent.parent
# Go up one more level to find .env in root
ROOT_DIR = BASE_DIR.parent

class Settings(BaseSettings):
    APP_NAME: str = "QueryFox"
    DEBUG: bool = False
    
    GROQ_API_KEY: str
    TAVILY_API_KEY: str

        # ✅ LangChain / LangSmith
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_PROJECT: str | None = None
    
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    TEMPERATURE: float = 0.3
    MAX_TOKENS: int = 2048
    
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RETRIEVAL_K: int = 3
    
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        # Look for .env in root directory
        env_file = str(ROOT_DIR / ".env")
        case_sensitive = True

settings = Settings()