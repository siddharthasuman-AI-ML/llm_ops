# SLM Training Platform UI

Streamlit-based UI for managing SLM training workflows.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file (see `docs/ENV_EXAMPLE.md`):
   ```env
   API_BASE_URL=http://localhost:8000
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Documentation

See the `docs/` folder for detailed documentation:
- `SETUP.md` - Installation and setup guide
- `API_INTEGRATION.md` - API integration details
- `ARCHITECTURE.md` - Architecture and design decisions
- `ENV_EXAMPLE.md` - Environment variables example

## Project Structure

- `app.py` - Main application entry point
- `pages/` - Page modules (home, datasets, models, experiments, evaluations, train_model)
- `services/` - API service layer
- `components/` - Reusable UI components
- `utils/` - Utility functions (config, validators, formatters)

## Features

- 📊 Dashboard with system overview
- 📁 Dataset management (upload, view, download)
- 🤖 Model browsing and details
- 🧪 Experiment tracking with auto-refresh
- 📈 Evaluation analysis with metrics and loss curves
- 🚀 Multi-step training wizard
