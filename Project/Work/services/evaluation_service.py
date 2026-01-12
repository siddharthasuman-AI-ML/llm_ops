"""Evaluation service for API calls related to evaluations."""

from typing import List, Dict, Any, Optional
from services.api_client import api_client, APIError


def get_evaluations(experiment_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all evaluations, optionally filtered by experiment.
    
    Args:
        experiment_id: Optional filter by experiment ID
        
    Returns:
        List of evaluation dictionaries
        
    Raises:
        APIError: If request fails
    """
    params = {}
    if experiment_id:
        params["experiment_id"] = experiment_id
    
    response = api_client.get("/evaluations", params=params)
    
    # Handle both list and dict responses
    if isinstance(response, list):
        return response
    elif isinstance(response, dict) and "evaluations" in response:
        return response["evaluations"]
    elif isinstance(response, dict) and "items" in response:
        return response["items"]
    else:
        return []


def get_evaluation(evaluation_id: str) -> Dict[str, Any]:
    """
    Get a specific evaluation by ID.
    
    Args:
        evaluation_id: ID of the evaluation
        
    Returns:
        Evaluation dictionary
        
    Raises:
        APIError: If request fails
    """
    return api_client.get(f"/evaluations/{evaluation_id}")
