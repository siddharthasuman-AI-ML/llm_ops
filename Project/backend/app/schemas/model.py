"""Model Pydantic schemas."""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ModelResponse(BaseModel):
    """Model response schema."""
    id: str
    name: str
    model_type: str
    version: Optional[str] = None
    architecture: Optional[str] = None
    parameters_count: Optional[int] = None
    created_at: Optional[datetime] = None
    is_latest_version: Optional[bool] = True
    
    class Config:
        from_attributes = True


class ModelDetailResponse(BaseModel):
    """Model detail response schema."""
    id: str
    name: str
    model_type: str
    base_model_id: Optional[str] = None
    version: Optional[str] = None
    architecture: Optional[str] = None
    parameters_count: Optional[int] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    is_latest_version: Optional[bool] = True
    created_at: Optional[datetime] = None
    linked_evaluations: Optional[List[str]] = None
    
    class Config:
        from_attributes = True
