"""Model API routes."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.model import Model, ModelType
from app.models.evaluation import Evaluation
from app.models.experiment import Experiment
from app.schemas.model import ModelResponse, ModelDetailResponse

router = APIRouter()


@router.get("", response_model=List[ModelResponse])
def get_models(
    model_type: Optional[str] = Query(None, description="Filter by model type: 'base' or 'fine_tuned'"),
    db: Session = Depends(get_db)
):
    """
    Get all models, optionally filtered by type.
    
    Args:
        model_type: Optional filter by model type
        db: Database session
        
    Returns:
        List of models
    """
    query = db.query(Model)
    
    if model_type:
        try:
            model_type_enum = ModelType(model_type.lower())
            query = query.filter(Model.model_type == model_type_enum)
        except ValueError:
            raise HTTPException(status_code=400, detail="model_type must be 'base' or 'fine_tuned'")
    
    models = query.all()
    return [
        ModelResponse(
            id=m.id,
            name=m.name,
            model_type=m.model_type.value,
            version=m.version,
            architecture=m.architecture,
            parameters_count=m.parameters_count,
            created_at=m.created_at,
            is_latest_version=m.is_latest_version
        )
        for m in models
    ]


@router.get("/{model_id}", response_model=ModelDetailResponse)
def get_model(model_id: str, db: Session = Depends(get_db)):
    """
    Get a specific model by ID.
    
    Args:
        model_id: Model ID
        db: Database session
        
    Returns:
        Model details
    """
    model = db.query(Model).filter(Model.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Get linked evaluations (evaluations for experiments that used this model as resulting model)
    experiments_with_model = db.query(Experiment).filter(
        Experiment.resulting_model_id == model_id
    ).all()
    
    linked_evaluations = []
    for exp in experiments_with_model:
        evals = db.query(Evaluation).filter(Evaluation.experiment_id == exp.id).all()
        linked_evaluations.extend([e.id for e in evals])
    
    linked_evaluations = linked_evaluations if linked_evaluations else None
    
    return ModelDetailResponse(
        id=model.id,
        name=model.name,
        model_type=model.model_type.value,
        base_model_id=model.base_model_id,
        version=model.version,
        architecture=model.architecture,
        parameters_count=model.parameters_count,
        description=model.description,
        metadata=model.model_metadata,
        is_latest_version=model.is_latest_version,
        created_at=model.created_at,
        linked_evaluations=linked_evaluations
    )
