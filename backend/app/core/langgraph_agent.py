from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from tavily import TavilyClient
import operator
import logging

from app.config import settings

logger = logging.getLogger(__name__)

llm = ChatGroq(
    model=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE,
    groq_api_key=settings.GROQ_API_KEY
)

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

class AgentState(TypedDict):
    query: str
    needs_search: bool
    search_results: str
    final_answer: str
    steps: Annotated[list[str], operator.add]

def analyze_query(state: AgentState) -> AgentState:
    query = state["query"]
    
    prompt = f"""Analyze if this query needs current web information or general knowledge.

Query: "{query}"

Respond with ONLY 'SEARCH' or 'DIRECT':
- SEARCH: Recent events, current data, news after 2023
- DIRECT: General knowledge, concepts, explanations

Response:"""
    
    try:
        response = llm.invoke(prompt)
        needs_search = "SEARCH" in response.content.upper()
        return {**state, "needs_search": needs_search, "steps": [f"Analyzed - Search: {needs_search}"]}
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return {**state, "needs_search": False, "steps": ["Analysis failed"]}

def search_web(state: AgentState) -> AgentState:
    try:
        search_response = tavily_client.search(query=state["query"], max_results=3)
        results = "\n\n".join([f"Source: {r['url']}\n{r['content']}" for r in search_response.get('results', [])])
        return {**state, "search_results": results, "steps": [f"Web search - {len(search_response.get('results', []))} sources"]}
    except Exception as e:
        logger.error(f"Search error: {e}")
        return {**state, "search_results": "", "steps": ["Search failed"]}

def synthesize_with_search(state: AgentState) -> AgentState:
    prompt = f"""Based on search results, answer the query.

Query: {state["query"]}

Search Results:
{state["search_results"]}

Answer:"""
    
    try:
        response = llm.invoke(prompt)
        return {**state, "final_answer": response.content, "steps": ["Synthesized from web"]}
    except Exception as e:
        logger.error(f"Synthesis error: {e}")
        return {**state, "final_answer": "Error generating answer", "steps": ["Synthesis failed"]}

def direct_answer(state: AgentState) -> AgentState:
    prompt = f"""Answer this query clearly:

Query: {state["query"]}

Answer:"""
    
    try:
        response = llm.invoke(prompt)
        return {**state, "final_answer": response.content, "steps": ["Direct answer"]}
    except Exception as e:
        logger.error(f"Direct answer error: {e}")
        return {**state, "final_answer": "Error generating answer", "steps": ["Failed"]}

def route_query(state: AgentState) -> Literal["search", "direct"]:
    return "search" if state["needs_search"] else "direct"

def create_agent_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("analyze", analyze_query)
    workflow.add_node("search", search_web)
    workflow.add_node("synthesize", synthesize_with_search)
    workflow.add_node("direct", direct_answer)
    workflow.set_entry_point("analyze")
    workflow.add_conditional_edges("analyze", route_query, {"search": "search", "direct": "direct"})
    workflow.add_edge("search", "synthesize")
    workflow.add_edge("synthesize", END)
    workflow.add_edge("direct", END)
    return workflow.compile()

agent_graph = create_agent_graph()