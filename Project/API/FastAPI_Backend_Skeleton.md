# Custom SLM Training Platform  
## FastAPI Backend Skeleton

---

## 1. Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Azure Blob SDK (or equivalent)
- Background task / external job trigger

---

## 2. Project Structure

backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── dataset.py
│   │   ├── model.py
│   │   ├── experiment.py
│   │   └── evaluation.py
│   ├── schemas/
│   │   ├── dataset.py
│   │   ├── model.py
│   │   ├── experiment.py
│   │   └── evaluation.py
│   ├── routes/
│   │   ├── datasets.py
│   │   ├── models.py
│   │   ├── experiments.py
│   │   └── evaluations.py
│   └── services/
│       ├── storage_service.py
│       ├── training_service.py
│       └── evaluation_service.py
├── requirements.txt
└── run.sh

---

## 3. main.py (Entry Point)

```python
from fastapi import FastAPI
from app.routes import datasets, models, experiments, evaluations

app = FastAPI(title="SLM Training Platform API")

app.include_router(datasets.router, prefix="/datasets")
app.include_router(models.router, prefix="/models")
app.include_router(experiments.router, prefix="/experiments")
app.include_router(evaluations.router, prefix="/evaluations")
