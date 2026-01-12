"""Base API client with error handling for the SLM Training Platform UI."""

import requests
from typing import Optional, Dict, Any
from requests.exceptions import RequestException, Timeout, ConnectionError as RequestsConnectionError

from utils.config import get_api_base_url


class APIError(Exception):
    """Custom exception for API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data


class APIClient:
    """Base API client for making HTTP requests to the backend."""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for the API. If not provided, uses config default.
        """
        self.base_url = base_url or get_api_base_url()
        self.timeout = 30  # 30 second timeout
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from endpoint.
        
        Args:
            endpoint: API endpoint (e.g., "/datasets")
            
        Returns:
            Full URL
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        
        return f"{self.base_url}{endpoint}"
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API response and extract JSON data.
        
        Args:
            response: HTTP response object
            
        Returns:
            JSON data from response
            
        Raises:
            APIError: If response indicates an error
        """
        try:
            response.raise_for_status()
            # Try to parse JSON
            if response.content:
                return response.json()
            return {}
        except requests.exceptions.HTTPError as e:
            # Try to extract error message from response
            error_message = f"API request failed: {e}"
            response_data = None
            
            try:
                response_data = response.json()
                if "detail" in response_data:
                    error_message = response_data["detail"]
                elif "message" in response_data:
                    error_message = response_data["message"]
            except (ValueError, KeyError):
                error_message = f"HTTP {response.status_code}: {response.text[:200]}"
            
            raise APIError(
                message=error_message,
                status_code=response.status_code,
                response_data=response_data
            )
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            APIError: If request fails
        """
        url = self._build_url(endpoint)
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            return self._handle_response(response)
        except Timeout:
            raise APIError("Request timed out. Please try again.")
        except RequestsConnectionError:
            raise APIError(
                f"Could not connect to API at {self.base_url}. "
                "Please check if the backend server is running."
            )
        except RequestException as e:
            raise APIError(f"Network error: {str(e)}")
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
             files: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            files: Files to upload (multipart/form-data)
            
        Returns:
            JSON response data
            
        Raises:
            APIError: If request fails
        """
        url = self._build_url(endpoint)
        
        try:
            if files:
                # Multipart form data (for file uploads)
                response = requests.post(
                    url,
                    data=data,
                    files=files,
                    timeout=self.timeout
                )
            elif json_data:
                # JSON data
                response = requests.post(
                    url,
                    json=json_data,
                    timeout=self.timeout
                )
            else:
                # Form data
                response = requests.post(
                    url,
                    data=data,
                    timeout=self.timeout
                )
            
            return self._handle_response(response)
        except Timeout:
            raise APIError("Request timed out. Please try again.")
        except RequestsConnectionError:
            raise APIError(
                f"Could not connect to API at {self.base_url}. "
                "Please check if the backend server is running."
            )
        except RequestException as e:
            raise APIError(f"Network error: {str(e)}")
    
    def download_file(self, endpoint: str, params: Optional[Dict] = None) -> bytes:
        """
        Download a file from the API.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            File content as bytes
            
        Raises:
            APIError: If request fails
        """
        url = self._build_url(endpoint)
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout, stream=True)
            response.raise_for_status()
            return response.content
        except Timeout:
            raise APIError("Request timed out. Please try again.")
        except RequestsConnectionError:
            raise APIError(
                f"Could not connect to API at {self.base_url}. "
                "Please check if the backend server is running."
            )
        except RequestException as e:
            raise APIError(f"Network error: {str(e)}")


# Global API client instance
api_client = APIClient()
