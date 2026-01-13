"""Model ORM model."""

import uuid
from sqlalchemy import Column, String, BigInteger, Boolean, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


class ModelType(str, enum.Enum):
    """Model type enumeration."""
    BASE = "base"
    FINE_TUNED = "fine_tuned"


class Model(Base):
    """Model model."""
    
    __tablename__ = "models"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    model_type = Column(SQLEnum(ModelType), nullable=False)
    base_model_id = Column(String, ForeignKey("models.id"), nullable=True)
    version = Column(String, nullable=True)
    architecture = Column(String, nullable=True)
    parameters_count = Column(BigInteger, nullable=True)
    description = Column(String, nullable=True)
    model_metadata = Column("metadata", JSON, nullable=True)  # Use "metadata" as DB column name
    is_latest_version = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    base_model = relationship("Model", remote_side=[id], backref="fine_tuned_models")
