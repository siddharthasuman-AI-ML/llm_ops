"""Dataset service for API calls related to datasets."""

from typing import List, Dict, Any, Optional
from services.api_client import api_client, APIError


def upload_dataset(
    file,
    name: str,
    description: str,
    dataset_type: str
) -> Dict[str, Any]:
    """
    Upload a dataset file.
    
    Args:
        file: Uploaded file object
        name: Dataset name
        description: Dataset description
        dataset_type: 'training' or 'evaluation'
        
    Returns:
        Dataset data from API response
        
    Raises:
        APIError: If upload fails
    """
    files = {"file": (file.name, file.getvalue(), file.type)}
    data = {
        "name": name,
        "description": description,
        "dataset_type": dataset_type
    }
    
    return api_client.post("/datasets/upload", data=data, files=files)


def get_datasets() -> List[Dict[str, Any]]:
    """
    Get all datasets.
    
    Returns:
        List of dataset dictionaries
        
    Raises:
        APIError: If request fails
    """
    response = api_client.get("/datasets")
    
    # Handle both list and dict responses
    if isinstance(response, list):
        return response
    elif isinstance(response, dict) and "datasets" in response:
        return response["datasets"]
    elif isinstance(response, dict) and "items" in response:
        return response["items"]
    else:
        return []


def download_dataset(dataset_id: str) -> bytes:
    """
    Download a dataset file.
    
    Args:
        dataset_id: ID of the dataset to download
        
    Returns:
        File content as bytes
        
    Raises:
        APIError: If download fails
    """
    return api_client.download_file(f"/datasets/{dataset_id}/download")
