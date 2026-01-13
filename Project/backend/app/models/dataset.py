"""Dataset ORM model."""

import uuid
from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum

from app.database import Base


class DatasetType(str, enum.Enum):
    """Dataset type enumeration."""
    TRAINING = "training"
    EVALUATION = "evaluation"


class Dataset(Base):
    """Dataset model."""
    
    __tablename__ = "datasets"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    dataset_type = Column(SQLEnum(DatasetType), nullable=False)
    file_path = Column(String, nullable=False)
    row_count = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
