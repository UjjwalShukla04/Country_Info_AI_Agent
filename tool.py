import requests
from typing import Dict, Any, Optional

class CountryDataTool:
    """
    A tool to fetch country data from the REST Countries API.
    """
    BASE_URL = "https://restcountries.com/v3.1/name/"

    @staticmethod
    def fetch_all() -> Dict[str, Any]:
        """
        Fetch data for all countries.
        """
        try:
            # We must specify fields to avoid payload size issues or API limitations
            # Fetching commonly used fields
            fields = "name,population,area,capital,currencies,region,languages,flags"
            url = f"https://restcountries.com/v3.1/all?fields={fields}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {"status": "success", "data": data}
            else:
                return {"status": "error", "message": f"API request failed with status code {response.status_code}."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def fetch_ranking(sort_by: str, limit: int = 5, ascending: bool = False) -> Dict[str, Any]:
        """
        Fetch ranking of countries based on a criteria.
        
        Args:
            sort_by: The field to sort by (e.g., 'population', 'area').
            limit: The number of countries to return.
            ascending: Whether to sort in ascending order.
        """
        result = CountryDataTool.fetch_all()
        if result["status"] != "success":
            return result
        
        countries = result["data"]
        
        # Helper to get value from country dict safely
        def get_value(country, field):
            if field == "population":
                return country.get("population", 0)
            elif field == "area":
                return country.get("area", 0)
            # Add more fields if needed
            return 0
            
        try:
            # Sort countries
            sorted_countries = sorted(
                countries, 
                key=lambda x: get_value(x, sort_by), 
                reverse=not ascending
            )
            
            # Take top N
            top_countries = sorted_countries[:limit]
            
            # Format result as a dict keyed by country name for consistency
            aggregated_data = {}
            for country in top_countries:
                name = country.get("name", {}).get("common", "Unknown")
                aggregated_data[name] = country
                
            return {"status": "success", "data": aggregated_data}
            
        except Exception as e:
            return {"status": "error", "message": f"Ranking failed: {str(e)}"}

    @staticmethod
    def fetch_data(country_name: str) -> Dict[str, Any]:
        """
        Fetch country data from the API.
        
        Args:
            country_name: The name of the country.
            
        Returns:
            A dictionary containing the country data or error information.
        """
        try:
            # Handle potential partial names or typos by using fuzzy matching in API if needed
            # For now, just direct match
            url = f"{CountryDataTool.BASE_URL}{country_name}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    # Filter for exact match first
                    query = country_name.lower()
                    
                    for country in data:
                        name_info = country.get("name", {})
                        common_name = name_info.get("common", "").lower()
                        official_name = name_info.get("official", "").lower()
                        alt_spellings = [alt.lower() for alt in country.get("altSpellings", [])]
                        cca2 = country.get("cca2", "").lower()
                        cca3 = country.get("cca3", "").lower()
                        cioc = country.get("cioc", "").lower()
                        
                        # Check for exact matches in various fields
                        if (query == common_name or 
                            query == official_name or 
                            query in alt_spellings or 
                            query == cca2 or 
                            query == cca3 or 
                            query == cioc):
                            return {"status": "success", "data": country}
                    
                    # If no exact match found, return the first result
                    return {"status": "success", "data": data[0]}
                else:
                    return {"status": "error", "message": "Country not found."}
            elif response.status_code == 404:
                return {"status": "error", "message": f"Country '{country_name}' not found."}
            else:
                return {"status": "error", "message": f"API request failed with status code {response.status_code}."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
