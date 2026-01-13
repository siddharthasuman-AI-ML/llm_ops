"""Experiment API routes."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.experiment import Experiment, ExperimentStatus
from app.models.model import Model
from app.models.dataset import Dataset
from app.schemas.experiment import ExperimentCreate, ExperimentResponse, ExperimentDetailResponse
from app.services.training_service import simulate_training

router = APIRouter()


@router.post("", response_model=ExperimentResponse, status_code=201)
async def create_experiment(
    experiment_data: ExperimentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new experiment (training job).
    
    Args:
        experiment_data: Experiment creation data
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Created experiment
    """
    # Validate base model exists
    base_model = db.query(Model).filter(Model.id == experiment_data.base_model_id).first()
    if not base_model:
        raise HTTPException(status_code=404, detail="Base model not found")
    
    # Validate training dataset exists
    training_dataset = db.query(Dataset).filter(Dataset.id == experiment_data.training_dataset_id).first()
    if not training_dataset:
        raise HTTPException(status_code=404, detail="Training dataset not found")
    
    # Validate eval dataset if provided
    if experiment_data.eval_dataset_id:
        eval_dataset = db.query(Dataset).filter(Dataset.id == experiment_data.eval_dataset_id).first()
        if not eval_dataset:
            raise HTTPException(status_code=404, detail="Evaluation dataset not found")
    
    # Create experiment
    experiment = Experiment(
        name=experiment_data.name,
        description=experiment_data.description,
        goal=experiment_data.goal,
        base_model_id=experiment_data.base_model_id,
        training_dataset_id=experiment_data.training_dataset_id,
        eval_dataset_id=experiment_data.eval_dataset_id,
        status=ExperimentStatus.CREATED,
        training_config=experiment_data.training_config
    )
    
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    
    # Start training simulation in background
    background_tasks.add_task(simulate_training, experiment.id)
    
    return ExperimentResponse(
        id=experiment.id,
        name=experiment.name,
        status=experiment.status.value,
        base_model_id=experiment.base_model_id,
        training_dataset_id=experiment.training_dataset_id,
        created_at=experiment.created_at
    )


@router.get("", response_model=List[ExperimentResponse])
def get_experiments(db: Session = Depends(get_db)):
    """
    Get all experiments.
    
    Args:
        db: Database session
        
    Returns:
        List of experiments
    """
    experiments = db.query(Experiment).all()
    return [
        ExperimentResponse(
            id=exp.id,
            name=exp.name,
            status=exp.status.value,
            base_model_id=exp.base_model_id,
            training_dataset_id=exp.training_dataset_id,
            created_at=exp.created_at
        )
        for exp in experiments
    ]


@router.get("/{experiment_id}", response_model=ExperimentDetailResponse)
def get_experiment(experiment_id: str, db: Session = Depends(get_db)):
    """
    Get a specific experiment by ID.
    
    Args:
        experiment_id: Experiment ID
        db: Database session
        
    Returns:
        Experiment details
    """
    experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    return ExperimentDetailResponse(
        id=experiment.id,
        name=experiment.name,
        description=experiment.description,
        goal=experiment.goal,
        base_model_id=experiment.base_model_id,
        training_dataset_id=experiment.training_dataset_id,
        eval_dataset_id=experiment.eval_dataset_id,
        status=experiment.status.value,
        training_config=experiment.training_config,
        resulting_model_id=experiment.resulting_model_id,
        created_at=experiment.created_at
    )
