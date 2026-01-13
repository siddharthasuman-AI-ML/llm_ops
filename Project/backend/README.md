# SLM Training Platform Backend API

FastAPI backend for the SLM Training Platform. Provides REST API endpoints for managing datasets, models, experiments, and evaluations.

## Features

- RESTful API with FastAPI
- SQLite database (no external database setup required)
- Local file storage for datasets
- Training job simulation
- Automatic database initialization
- Sample base models seeded on first run
- CORS enabled for Streamlit UI integration

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**Or manually:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Verify Installation

Open your browser and navigate to:
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`
- Root Endpoint: `http://localhost:8000/`

## API Endpoints

### Datasets
- `POST /datasets/upload` - Upload a dataset file
- `GET /datasets` - List all datasets
- `GET /datasets/{id}/download` - Download a dataset file

### Models
- `GET /models` - List all models (optional: `?model_type=base`)
- `GET /models/{id}` - Get model details

### Experiments
- `POST /experiments` - Create a new experiment (training job)
- `GET /experiments` - List all experiments
- `GET /experiments/{id}` - Get experiment details

### Evaluations
- `GET /evaluations` - List all evaluations (optional: `?experiment_id=...`)
- `GET /evaluations/{id}` - Get evaluation details

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic schemas
│   ├── routes/              # API route handlers
│   └── services/            # Business logic services
├── uploads/                 # Uploaded dataset files
├── database.db              # SQLite database (created automatically)
├── requirements.txt         # Python dependencies
├── run.bat                  # Windows startup script
└── run.sh                   # Linux/Mac startup script
```

## Configuration

Configuration is managed in `app/config.py`. Key settings:

- `database_url`: SQLite database path (default: `sqlite:///./database.db`)
- `upload_dir`: Directory for uploaded files (default: `./uploads`)
- `cors_origins`: Allowed CORS origins (includes Streamlit default ports)
- `training_simulation_delay`: Seconds before training starts (default: 5)
- `training_simulation_duration`: Training simulation duration (default: 30)

## Database

The backend uses SQLite by default, which requires no setup. The database file (`database.db`) is created automatically on first run.

Tables are created automatically on startup:
- `datasets` - Dataset metadata
- `models` - Model information
- `experiments` - Training experiments
- `evaluations` - Evaluation results

## File Storage

Uploaded dataset files are stored in the `uploads/` directory. Files are named using the pattern: `{dataset_id}_{original_filename}`.

Supported file formats:
- CSV (`.csv`)
- JSON (`.json`)
- JSONL (`.jsonl`)

## Training Simulation

Since actual training happens externally, the backend simulates training jobs:

1. Experiment created with status "created"
2. After delay, status changes to "running"
3. After simulation duration, status changes to "completed" or "failed"
4. On completion, creates evaluation with mock metrics and loss curves
5. Creates resulting fine-tuned model

## Sample Data

On first run, the backend automatically seeds the database with sample base models:
- GPT-2 Small (124M parameters)
- GPT-2 Medium (355M parameters)
- BERT Base (110M parameters)

## Development

### Running in Development Mode

The server runs with `--reload` flag by default, which automatically restarts on code changes.

### Testing Endpoints

Use the interactive API documentation at `http://localhost:8000/docs` to test endpoints.

### Database Reset

To reset the database, simply delete `database.db` and restart the server.

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, change it in `run.bat` or `run.sh`:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### Import Errors

Ensure you're running from the `backend/` directory:
```bash
cd backend
uvicorn app.main:app --reload
```

### Database Errors

If you encounter database errors:
1. Delete `database.db`
2. Restart the server (tables will be recreated)

## Integration with Streamlit UI

The backend is configured to work with the Streamlit UI:
1. Ensure backend is running on `http://localhost:8000`
2. Streamlit UI should have `API_BASE_URL=http://localhost:8000` in `.env` file
3. CORS is configured to allow requests from Streamlit (ports 8501, 8502)

## Next Steps

1. Start the backend server
2. Verify it's running at `http://localhost:8000/docs`
3. Start the Streamlit UI (see `work/README.md`)
4. Test the full workflow:
   - Upload a dataset
   - Create an experiment
   - Monitor training progress
   - View evaluation results
