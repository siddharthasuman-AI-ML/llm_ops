"""Dataset API routes."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from app.database import get_db
from app.models.dataset import Dataset, DatasetType
from app.schemas.dataset import DatasetResponse, DatasetCreate
from app.services.storage_service import save_uploaded_file

router = APIRouter()


@router.post("/upload", response_model=DatasetResponse, status_code=201)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(None),
    dataset_type: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Upload a dataset file.
    
    Args:
        file: Uploaded file
        name: Dataset name
        description: Dataset description
        dataset_type: 'training' or 'evaluation'
        db: Database session
        
    Returns:
        Created dataset
    """
    # Validate dataset type
    try:
        dataset_type_enum = DatasetType(dataset_type.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="dataset_type must be 'training' or 'evaluation'")
    
    # Create dataset record first to get ID
    dataset = Dataset(
        name=name,
        description=description,
        dataset_type=dataset_type_enum,
        file_path=""  # Will be updated
    )
    db.add(dataset)
    db.flush()  # Get the ID
    
    try:
        # Save file
        file_path, row_count = save_uploaded_file(file, dataset.id)
        dataset.file_path = file_path
        dataset.row_count = row_count
        db.commit()
        db.refresh(dataset)
        
        # Format response
        return DatasetResponse(
            id=dataset.id,
            name=dataset.name,
            description=dataset.description,
            dataset_type=dataset.dataset_type.value,
            row_count=dataset.row_count,
            upload_date=dataset.created_at.isoformat() if dataset.created_at else None,
            created_at=dataset.created_at
        )
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload dataset: {str(e)}")


@router.get("", response_model=List[DatasetResponse])
def get_datasets(db: Session = Depends(get_db)):
    """
    Get all datasets.
    
    Args:
        db: Database session
        
    Returns:
        List of datasets
    """
    datasets = db.query(Dataset).all()
    return [
        DatasetResponse(
            id=ds.id,
            name=ds.name,
            description=ds.description,
            dataset_type=ds.dataset_type.value,
            row_count=ds.row_count,
            upload_date=ds.created_at.isoformat() if ds.created_at else None,
            created_at=ds.created_at
        )
        for ds in datasets
    ]


@router.get("/{dataset_id}/download")
def download_dataset(dataset_id: str, db: Session = Depends(get_db)):
    """
    Download a dataset file.
    
    Args:
        dataset_id: Dataset ID
        db: Database session
        
    Returns:
        File download response
    """
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    file_path = Path(dataset.file_path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=dataset.name + file_path.suffix,
        media_type="application/octet-stream"
    )
