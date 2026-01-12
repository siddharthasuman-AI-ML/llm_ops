"""Model service for API calls related to models."""

from typing import List, Dict, Any, Optional
from services.api_client import api_client, APIError


def get_models(model_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all models, optionally filtered by type.
    
    Args:
        model_type: Optional filter by 'base' or 'fine_tuned'
        
    Returns:
        List of model dictionaries
        
    Raises:
        APIError: If request fails
    """
    params = {}
    if model_type:
        params["model_type"] = model_type
    
    response = api_client.get("/models", params=params)
    
    # Handle both list and dict responses
    if isinstance(response, list):
        return response
    elif isinstance(response, dict) and "models" in response:
        return response["models"]
    elif isinstance(response, dict) and "items" in response:
        return response["items"]
    else:
        return []


def get_model(model_id: str) -> Dict[str, Any]:
    """
    Get a specific model by ID.
    
    Args:
        model_id: ID of the model
        
    Returns:
        Model dictionary
        
    Raises:
        APIError: If request fails
    """
    return api_client.get(f"/models/{model_id}")
