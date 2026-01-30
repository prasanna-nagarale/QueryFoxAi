from langchain_groq import ChatGroq
from typing import Dict, Optional
import logging
import pickle
import base64

from app.config import settings
from app.core.langgraph_agent import agent_graph

logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self):
        self.llm = ChatGroq(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            groq_api_key=settings.GROQ_API_KEY
        )
    
    async def query(self, query: str, vectorstore_data: Optional[str]) -> Dict:
        if vectorstore_data:
            return await self._rag_query(query, vectorstore_data)
        else:
            return await self._agent_query(query)
    
    async def _rag_query(self, query: str, vectorstore_data: str) -> Dict:
        try:
            vectorstore = pickle.loads(base64.b64decode(vectorstore_data))
            docs = vectorstore.similarity_search(query, k=settings.RETRIEVAL_K)
            
            if not docs:
                return await self._agent_query(query)
            
            context = "\n\n".join([f"Chunk {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
            
            prompt = f"""Answer based on the provided context. If not found, say so.

Query: {query}

Context:
{context}

Answer:"""
            
            response = self.llm.invoke(prompt)
            
            return {
                "answer": response.content,
                "sources": [{"content": doc.page_content[:200], "metadata": doc.metadata} for doc in docs],
                "steps": ["Retrieved from documents", "Generated answer"],
                "needs_search": False
            }
        except Exception as e:
            logger.error(f"RAG error: {e}")
            return {"answer": "Error processing query", "sources": [], "steps": ["Error"], "needs_search": False}
    
    async def _agent_query(self, query: str) -> Dict:
        try:
            initial_state = {"query": query, "needs_search": False, "search_results": "", "final_answer": "", "steps": []}
            result = agent_graph.invoke(initial_state)
            return {
                "answer": result["final_answer"],
                "sources": None,
                "steps": result["steps"],
                "needs_search": result["needs_search"]
            }
        except Exception as e:
            logger.error(f"Agent error: {e}")
            return {"answer": "Error processing query", "sources": None, "steps": ["Error"], "needs_search": False}

rag_engine = RAGEngine()