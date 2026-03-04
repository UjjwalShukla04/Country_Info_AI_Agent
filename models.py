from typing import List, Optional
from pydantic import BaseModel, Field

class Intent(BaseModel):
    """
    Extracted intent from the user question.
    """
    country_names: List[str] = Field(default_factory=list, description="The names of the countries mentioned in the question. If no specific country is mentioned (e.g., for ranking 'top 5 countries'), this list can be empty.")
    requested_fields: List[str] = Field(default_factory=list, description="The specific information requested about the countries (e.g., 'population', 'capital', 'currency'). If general information is requested, use ['general'].")
    is_comparison: bool = Field(default=False, description="Whether the user wants to compare multiple countries.")
    is_summary: bool = Field(default=False, description="Whether the user wants a general summary or overview of a country.")
    is_ranking: bool = Field(default=False, description="Whether the user wants to rank or list top/bottom countries (e.g., 'top 5 populated').")
    limit: int = Field(default=5, description="The number of countries to list/rank (e.g., 5 for 'top 5').")
    sort_by: str = Field(default="population", description="The criteria to sort by (e.g., 'population', 'area'). Default to 'population' if not specified.")
