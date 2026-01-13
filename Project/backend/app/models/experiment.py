"""Experiment ORM model."""

import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class ExperimentStatus(str, enum.Enum):
    """Experiment status enumeration."""
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Experiment(Base):
    """Experiment model."""
    
    __tablename__ = "experiments"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    base_model_id = Column(String, ForeignKey("models.id"), nullable=False)
    training_dataset_id = Column(String, ForeignKey("datasets.id"), nullable=False)
    eval_dataset_id = Column(String, ForeignKey("datasets.id"), nullable=True)
    status = Column(SQLEnum(ExperimentStatus), nullable=False, default=ExperimentStatus.CREATED)
    training_config = Column(JSON, nullable=False)
    resulting_model_id = Column(String, ForeignKey("models.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    base_model = relationship("Model", foreign_keys=[base_model_id])
    training_dataset = relationship("Dataset", foreign_keys=[training_dataset_id])
    eval_dataset = relationship("Dataset", foreign_keys=[eval_dataset_id])
    resulting_model = relationship("Model", foreign_keys=[resulting_model_id])
    evaluations = relationship("Evaluation", back_populates="experiment")
