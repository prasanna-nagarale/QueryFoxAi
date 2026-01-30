from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from typing import Tuple
import tempfile
import os
import logging
import pickle
import base64

from app.config import settings
from app.core.embeddings import embedding_manager

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
    
    async def process_file(self, file_content: bytes, filename: str) -> Tuple[str, int]:
        suffix = filename.split(".")[-1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        try:
            loader = self._get_loader(tmp_path, suffix)
            documents = loader.load()
            
            if not documents:
                raise ValueError("No content extracted from file")
            
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Created {len(chunks)} chunks from {filename}")
            
            embeddings = embedding_manager.get_embeddings()
            vectorstore = FAISS.from_documents(chunks, embeddings)
            
            serialized = base64.b64encode(pickle.dumps(vectorstore)).decode('utf-8')
            
            return serialized, len(chunks)
            
        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass
    
    def _get_loader(self, file_path: str, suffix: str):
        loaders = {
            "pdf": PyPDFLoader,
            "txt": lambda p: TextLoader(p, encoding='utf-8'),
            "csv": CSVLoader,
            "docx": UnstructuredWordDocumentLoader,
            "doc": UnstructuredWordDocumentLoader,
        }
        
        loader_class = loaders.get(suffix)
        if not loader_class:
            raise ValueError(f"Unsupported file type: {suffix}")
        
        return loader_class(file_path)

document_processor = DocumentProcessor()