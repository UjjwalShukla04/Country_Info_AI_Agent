from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnableLambda

from state import AgentState
from models import Intent
from tool import CountryDataTool

# Define the LLM (using a placeholder for now, ideally configured via env vars)
# Assuming OPENAI_API_KEY is set in environment or user will provide it.
try:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
except Exception as e:
    print(f"Warning: Failed to initialize LLM: {e}")
    llm = None

# Define the intent extraction prompt
intent_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that identifies the countries and the requested information from a user's question. 
    Extract the country names and the requested fields. 
    Set 'is_comparison' to True if the user asks to compare countries. 
    Set 'is_summary' to True if the user asks for a general summary or overview of a country (e.g., 'Tell me about Germany', 'Summary of France').
    Set 'is_ranking' to True if the user asks to rank or list top/bottom countries (e.g., 'top 5 populated', 'most populated countries').
    If 'is_ranking' is True:
    - Set 'limit' to the number of countries requested (default to 5).
    - Set 'sort_by' to the sorting criteria (e.g., 'population', 'area').
    """),
    ("human", "{question}")
])

# Define the intent extraction chain
intent_parser = PydanticOutputParser(pydantic_object=Intent)
if llm:
    # Use method="function_calling" for gpt-3.5-turbo compatibility
    intent_chain = intent_prompt | llm.with_structured_output(Intent, method="function_calling")
else:
    intent_chain = None

def identify_intent(state: AgentState) -> Dict[str, Any]:
    """
    Identifies the countries and requested fields from the user question.
    """
    if not intent_chain:
        return {"error": "LLM not initialized. Please set OPENAI_API_KEY."}
        
    question = state["question"]
    try:
        intent = intent_chain.invoke({"question": question})
        if not intent:
             return {"error": "Could not identify country or intent from the question."}
        
        return {
            "country_names": intent.country_names,
            "requested_fields": intent.requested_fields,
            "is_comparison": intent.is_comparison,
            "is_summary": intent.is_summary,
            "is_ranking": intent.is_ranking,
            "limit": intent.limit,
            "sort_by": intent.sort_by,
            "error": None
        }
    except Exception as e:
        return {"error": f"Intent identification failed: {str(e)}"}

def invoke_tool(state: AgentState) -> Dict[str, Any]:
    """
    Invokes the country data tool to fetch information for multiple countries.
    """
    if state.get("error"):
        return {"raw_data": None}
    
    is_ranking = state.get("is_ranking", False)
    
    if is_ranking:
        limit = state.get("limit", 5)
        sort_by = state.get("sort_by", "population")
        # Default to descending for population/area
        ascending = False
        
        try:
            tool = CountryDataTool()
            result = tool.fetch_ranking(sort_by=sort_by, limit=limit, ascending=ascending)
            if result.get("status") == "success":
                return {"raw_data": result.get("data"), "error": None}
            else:
                return {"error": result.get("message"), "raw_data": None}
        except Exception as e:
            return {"error": f"Ranking tool failed: {str(e)}", "raw_data": None}

    country_names = state.get("country_names")
    if not country_names:
        return {"error": "No country names identified."}
    
    aggregated_data = {}
    errors = []
    
    try:
        tool = CountryDataTool()
        for country in country_names:
            result = tool.fetch_data(country)
            if result.get("status") == "success":
                aggregated_data[country] = result.get("data")
            else:
                aggregated_data[country] = {"error": result.get("message")}
                # We record the error but continue for other countries
        
        return {"raw_data": aggregated_data, "error": None}
    except Exception as e:
        return {"error": f"Tool invocation failed: {str(e)}", "raw_data": None}

# Define the synthesis prompt
synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant that answers questions about countries based on the provided data.
    
    If the user's intent is a comparison (is_comparison=True) or a ranking (is_ranking=True):
    - You MUST output the data in a Markdown table.
    - Columns should be the country names and rows should be the requested fields (or key data points).
    - If it is a ranking, include the rank number.

    If the user's intent is a summary (is_summary=True) or "general" information is requested:
    - You MUST provide a comprehensive overview including:
      - Capital
      - Population
      - Region/Subregion
      - Currency
      - Languages
      - A brief description or interesting facts if available.
    - Use bullet points for readability.
    
    If the data contains a flag URL (usually in 'flags.png' or 'flags.svg'), you MUST include the flag image at the end of your response using Markdown syntax: ![Flag of Country](flag_url).
    
    If data is missing or incomplete, state that clearly."""),
    ("human", "Question: {question}\nData: {raw_data}\nRequested Fields: {requested_fields}\nIs Comparison: {is_comparison}\nIs Summary: {is_summary}")
])

if llm:
    synthesis_chain = synthesis_prompt | llm
else:
    synthesis_chain = None

def synthesize_answer(state: AgentState) -> Dict[str, Any]:
    """
    Synthesizes the final answer based on the tool output.
    """
    if not synthesis_chain:
        return {"answer": "Error: LLM not initialized. Please set OPENAI_API_KEY."}

    if state.get("error"):
        return {"answer": f"I encountered an error: {state['error']}"}
    
    question = state["question"]
    raw_data = state["raw_data"]
    requested_fields = state["requested_fields"]
    is_comparison = state.get("is_comparison", False)
    is_summary = state.get("is_summary", False)
    is_ranking = state.get("is_ranking", False)
    
    if not raw_data:
        return {"answer": "I could not find data for the requested countries."}
        
    try:
        response = synthesis_chain.invoke({
            "question": question,
            "raw_data": raw_data,
            "requested_fields": requested_fields,
            "is_comparison": is_comparison,
            "is_summary": is_summary,
            "is_ranking": is_ranking
        })
        return {"answer": response.content}
    except Exception as e:
        return {"answer": f"Failed to generate answer: {str(e)}"}
