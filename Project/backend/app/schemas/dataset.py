"""Dataset Pydantic schemas."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DatasetResponse(BaseModel):
    """Dataset response schema."""
    id: str
    name: str
    description: Optional[str] = None
    dataset_type: str
    row_count: Optional[int] = None
    upload_date: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DatasetCreate(BaseModel):
    """Dataset creation schema."""
    name: str
    description: Optional[str] = None
    dataset_type: str
