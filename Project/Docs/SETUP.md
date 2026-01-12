# SLM Training Platform UI - Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Access to the backend API (or mock backend for testing)

## Installation

### 1. Navigate to the work directory

```bash
cd work
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the `work` directory (or copy from `.env.example`):

```bash
API_BASE_URL=http://localhost:8000
```

Replace `http://localhost:8000` with your actual backend API URL.

## Running the Application

### Start the Streamlit app

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Running with custom port

```bash
streamlit run app.py --server.port 8502
```

## Project Structure

```
work/
├── app.py                 # Main application entry point
├── pages/                 # Page modules
│   ├── home.py
│   ├── datasets.py
│   ├── models.py
│   ├── experiments.py
│   ├── evaluations.py
│   └── train_model.py
├── services/             # API service layer
│   ├── api_client.py
│   ├── dataset_service.py
│   ├── model_service.py
│   ├── experiment_service.py
│   └── evaluation_service.py
├── components/           # Reusable UI components
│   ├── navigation.py
│   ├── status_badge.py
│   ├── loading_spinner.py
│   ├── error_message.py
│   └── empty_state.py
├── utils/                # Utility functions
│   ├── config.py
│   ├── validators.py
│   └── formatters.py
└── requirements.txt      # Python dependencies
```

## Troubleshooting

### API Connection Issues

If you see "Could not connect to API" errors:

1. Verify the backend API is running
2. Check the `API_BASE_URL` in your `.env` file
3. Ensure the URL is correct (including protocol: `http://` or `https://`)
4. Check firewall/network settings

### Import Errors

If you encounter import errors:

1. Ensure you're in the `work` directory
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Check that Python path includes the work directory

### Port Already in Use

If port 8501 is already in use:

```bash
streamlit run app.py --server.port 8502
```

## Development

### Running in Development Mode

For auto-reload on code changes:

```bash
streamlit run app.py --server.runOnSave true
```

### Debugging

Enable debug mode by setting environment variable:

```bash
# Windows
set STREAMLIT_LOGGER_LEVEL=debug
streamlit run app.py

# Linux/Mac
export STREAMLIT_LOGGER_LEVEL=debug
streamlit run app.py
```

## Next Steps

1. Ensure your backend API is running and accessible
2. Test the connection by navigating to the Home page
3. Upload a dataset to get started
4. Create your first experiment using the Train Model wizard
