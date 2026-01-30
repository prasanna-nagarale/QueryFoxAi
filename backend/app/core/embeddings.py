from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingManager:
    _instance = None
    _embeddings = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_embeddings(self):
        if self._embeddings is None:
            logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
            self._embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        return self._embeddings

embedding_manager = EmbeddingManager()