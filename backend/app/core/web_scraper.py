import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from typing import Tuple, List, Dict
import logging
import pickle
import base64

from app.config import settings
from app.core.embeddings import embedding_manager
from app.core.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.visited_urls = set()
    
    async def scrape_url(self, base_url: str, max_pages: int = 1) -> Tuple[str, int, int]:
        self.visited_urls.clear()
        structured_content = []
        
        self._scrape_recursive(base_url, max_pages, structured_content)
        
        if not structured_content:
            raise ValueError("No content extracted from website")
        
        combined_text = self._format_structured_content(structured_content)
        documents = [Document(
            page_content=combined_text,
            metadata={"source": base_url, "pages_scraped": len(self.visited_urls)}
        )]
        
        chunks = self.doc_processor.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks from {len(self.visited_urls)} pages")
        
        embeddings = embedding_manager.get_embeddings()
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        serialized = base64.b64encode(pickle.dumps(vectorstore)).decode('utf-8')
        
        return serialized, len(chunks), len(self.visited_urls)
    
    def _scrape_recursive(self, url: str, max_pages: int, all_content: List, depth: int = 0):
        if len(self.visited_urls) >= max_pages or depth > 2 or url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        
        try:
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                tag.decompose()
            
            page_content = self._extract_structured_content(soup)
            if page_content:
                all_content.append(page_content)
            
            if depth < 2 and len(self.visited_urls) < max_pages:
                base_domain = urlparse(url).netloc
                for a_tag in soup.find_all('a', href=True):
                    link = urljoin(url, a_tag['href']).split('#')[0]
                    if urlparse(link).netloc == base_domain:
                        self._scrape_recursive(link, max_pages, all_content, depth + 1)
        
        except Exception as e:
            logger.warning(f"Error scraping {url}: {str(e)}")
    
    def _extract_structured_content(self, soup) -> Dict:
        content = {
            "headings": [],
            "paragraphs": [],
            "lists": []
        }
        
        for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text and len(text) > 5:
                    content["headings"].append({"level": tag, "text": text})
        
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text and len(text) > 30:
                content["paragraphs"].append(text)
        
        for ul in soup.find_all(['ul', 'ol']):
            items = [li.get_text(strip=True) for li in ul.find_all('li') if li.get_text(strip=True)]
            if items:
                content["lists"].append(items)
        
        return content if (content["headings"] or content["paragraphs"] or content["lists"]) else None
    
    def _format_structured_content(self, structured_content: List[Dict]) -> str:
        formatted = []
        
        for page in structured_content:
            if page["headings"]:
                formatted.append("\n=== HEADINGS ===")
                for h in page["headings"]:
                    formatted.append(f"{h['level'].upper()}: {h['text']}")
            
            if page["paragraphs"]:
                formatted.append("\n=== CONTENT ===")
                formatted.extend(page["paragraphs"])
            
            if page["lists"]:
                formatted.append("\n=== LISTS ===")
                for lst in page["lists"]:
                    for item in lst:
                        formatted.append(f"• {item}")
        
        return "\n\n".join(formatted)

web_scraper = WebScraper()