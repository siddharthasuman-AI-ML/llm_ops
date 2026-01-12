"""Configuration management for the SLM Training Platform UI."""

import os
from typing import Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Ensure API_BASE_URL doesn't end with a slash
if API_BASE_URL.endswith("/"):
    API_BASE_URL = API_BASE_URL.rstrip("/")


def get_api_base_url() -> str:
    """Get the API base URL from environment variables."""
    return API_BASE_URL


def validate_config() -> Tuple[bool, str]:
    """
    Validate that required configuration is present.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not API_BASE_URL:
        return False, "API_BASE_URL environment variable is not set. Please set it in your .env file."
    
    if not API_BASE_URL.startswith(("http://", "https://")):
        return False, f"API_BASE_URL must start with http:// or https://. Got: {API_BASE_URL}"
    
    return True, ""
