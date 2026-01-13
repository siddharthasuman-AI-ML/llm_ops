"""Evaluation Pydantic schemas."""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class EvaluationResponse(BaseModel):
    """Evaluation response schema."""
    id: str
    experiment_id: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EvaluationDetailResponse(BaseModel):
    """Evaluation detail response schema."""
    id: str
    experiment_id: str
    metrics: Dict[str, Any]
    loss_curve: Optional[Dict[str, Any]] = None
    training_statistics: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
