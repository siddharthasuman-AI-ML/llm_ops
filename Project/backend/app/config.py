"""Configuration management for the backend API."""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "sqlite:///./database.db"
    
    # File storage
    upload_dir: str = "./uploads"
    
    # API
    api_title: str = "SLM Training Platform API"
    api_version: str = "1.0.0"
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:8501",  # Streamlit default port
        "http://localhost:8502",
        "http://127.0.0.1:8501",
        "http://127.0.0.1:8502",
    ]
    
    # Training simulation
    training_simulation_delay: int = 5  # seconds before status changes to "running"
    training_simulation_duration: int = 30  # seconds to simulate training
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Ensure upload directory exists
upload_path = Path(settings.upload_dir)
upload_path.mkdir(parents=True, exist_ok=True)

# Database path
db_path = Path(settings.database_url.replace("sqlite:///", ""))
db_path.parent.mkdir(parents=True, exist_ok=True)
