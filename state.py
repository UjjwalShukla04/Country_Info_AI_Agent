from typing import TypedDict, Optional, List, Dict, Any
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """
    State for the Country Information Agent.
    """
    question: str  # The original user question
    
    # Extracted intent
    country_names: Optional[List[str]]
    requested_fields: Optional[List[str]]  # e.g., ["population", "capital"]
    is_comparison: Optional[bool]
    is_summary: Optional[bool]
    is_ranking: Optional[bool]
    limit: Optional[int]
    sort_by: Optional[str]
    
    # Tool output
    raw_data: Optional[Dict[str, Any]]  # Mapping of country name to data

    
    # Final output
    answer: Optional[str]
    
    # Error handling
    error: Optional[str]
    
    # Message history (optional for simple flow but good for LangGraph debugging)
    messages: List[BaseMessage]
