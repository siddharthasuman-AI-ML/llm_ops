"""Evaluation API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.evaluation import Evaluation
from app.schemas.evaluation import EvaluationResponse, EvaluationDetailResponse

router = APIRouter()


@router.get("", response_model=List[EvaluationResponse])
def get_evaluations(
    experiment_id: Optional[str] = Query(None, description="Filter by experiment ID"),
    db: Session = Depends(get_db)
):
    """
    Get all evaluations, optionally filtered by experiment.
    
    Args:
        experiment_id: Optional filter by experiment ID
        db: Database session
        
    Returns:
        List of evaluations
    """
    query = db.query(Evaluation)
    
    if experiment_id:
        query = query.filter(Evaluation.experiment_id == experiment_id)
    
    evaluations = query.all()
    return [
        EvaluationResponse(
            id=eval.id,
            experiment_id=eval.experiment_id,
            created_at=eval.created_at
        )
        for eval in evaluations
    ]


@router.get("/{evaluation_id}", response_model=EvaluationDetailResponse)
def get_evaluation(evaluation_id: str, db: Session = Depends(get_db)):
    """
    Get a specific evaluation by ID.
    
    Args:
        evaluation_id: Evaluation ID
        db: Database session
        
    Returns:
        Evaluation details
    """
    evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return EvaluationDetailResponse(
        id=evaluation.id,
        experiment_id=evaluation.experiment_id,
        metrics=evaluation.metrics,
        loss_curve=evaluation.loss_curve,
        training_statistics=evaluation.training_statistics,
        created_at=evaluation.created_at
    )
