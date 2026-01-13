"""Experiment Pydantic schemas."""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ExperimentCreate(BaseModel):
    """Experiment creation schema."""
    name: str
    description: Optional[str] = None
    goal: Optional[str] = None
    base_model_id: str
    training_dataset_id: str
    eval_dataset_id: Optional[str] = None
    training_config: Dict[str, Any]


class ExperimentResponse(BaseModel):
    """Experiment response schema."""
    id: str
    name: str
    status: str
    base_model_id: str
    training_dataset_id: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ExperimentDetailResponse(BaseModel):
    """Experiment detail response schema."""
    id: str
    name: str
    description: Optional[str] = None
    goal: Optional[str] = None
    base_model_id: str
    training_dataset_id: str
    eval_dataset_id: Optional[str] = None
    status: str
    training_config: Dict[str, Any]
    resulting_model_id: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
