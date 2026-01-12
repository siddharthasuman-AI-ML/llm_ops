"""Experiment service for API calls related to experiments."""

from typing import List, Dict, Any, Optional
from services.api_client import api_client, APIError


def create_experiment(
    name: str,
    description: str,
    goal: str,
    base_model_id: str,
    training_dataset_id: str,
    eval_dataset_id: Optional[str],
    learning_rate: float,
    epochs: int,
    batch_size: int
) -> Dict[str, Any]:
    """
    Create a new experiment (training job).
    
    Args:
        name: Experiment name
        description: Experiment description
        goal: Experiment goal
        base_model_id: ID of the base model
        training_dataset_id: ID of the training dataset
        eval_dataset_id: Optional ID of the evaluation dataset
        learning_rate: Learning rate for training
        epochs: Number of training epochs
        batch_size: Batch size for training
        
    Returns:
        Experiment data from API response
        
    Raises:
        APIError: If creation fails
    """
    training_config = {
        "learning_rate": learning_rate,
        "epochs": epochs,
        "batch_size": batch_size
    }
    
    json_data = {
        "name": name,
        "description": description,
        "goal": goal,
        "base_model_id": base_model_id,
        "training_dataset_id": training_dataset_id,
        "eval_dataset_id": eval_dataset_id,
        "training_config": training_config
    }
    
    return api_client.post("/experiments", json_data=json_data)


def get_experiments() -> List[Dict[str, Any]]:
    """
    Get all experiments.
    
    Returns:
        List of experiment dictionaries
        
    Raises:
        APIError: If request fails
    """
    response = api_client.get("/experiments")
    
    # Handle both list and dict responses
    if isinstance(response, list):
        return response
    elif isinstance(response, dict) and "experiments" in response:
        return response["experiments"]
    elif isinstance(response, dict) and "items" in response:
        return response["items"]
    else:
        return []


def get_experiment(experiment_id: str) -> Dict[str, Any]:
    """
    Get a specific experiment by ID.
    
    Args:
        experiment_id: ID of the experiment
        
    Returns:
        Experiment dictionary
        
    Raises:
        APIError: If request fails
    """
    return api_client.get(f"/experiments/{experiment_id}")
