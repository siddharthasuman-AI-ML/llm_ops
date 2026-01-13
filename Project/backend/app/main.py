"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db, SessionLocal
from app.routes import datasets, models, experiments, evaluations
from app.models.model import Model, ModelType

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API for SLM Training Platform"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
app.include_router(models.router, prefix="/models", tags=["models"])
app.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
app.include_router(evaluations.router, prefix="/evaluations", tags=["evaluations"])


@app.on_event("startup")
async def startup_event():
    """Initialize database and create tables on startup."""
    init_db()
    
    # Seed sample base models if database is empty
    db = SessionLocal()
    try:
        existing_models = db.query(Model).filter(Model.model_type == ModelType.BASE).count()
        if existing_models == 0:
            sample_models = [
                Model(
                    name="GPT-2 Small",
                    model_type=ModelType.BASE,
                    version="1.0",
                    architecture="transformer",
                    parameters_count=124000000,
                    description="Small GPT-2 model for fine-tuning",
                    is_latest_version=True
                ),
                Model(
                    name="GPT-2 Medium",
                    model_type=ModelType.BASE,
                    version="1.0",
                    architecture="transformer",
                    parameters_count=355000000,
                    description="Medium GPT-2 model for fine-tuning",
                    is_latest_version=True
                ),
                Model(
                    name="BERT Base",
                    model_type=ModelType.BASE,
                    version="1.0",
                    architecture="transformer",
                    parameters_count=110000000,
                    description="BERT base model for fine-tuning",
                    is_latest_version=True
                ),
            ]
            for model in sample_models:
                db.add(model)
            db.commit()
            print("Sample base models seeded")
    finally:
        db.close()
    
    print("Database initialized")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "SLM Training Platform API",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
