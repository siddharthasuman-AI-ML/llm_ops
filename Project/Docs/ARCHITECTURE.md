# SLM Training Platform UI - Architecture Documentation

## Overview

The SLM Training Platform UI is a Streamlit-based web application that provides a control plane for managing SLM training workflows. The UI is completely API-driven and contains no business logic - all operations are delegated to the backend API.

## Architecture Principles

1. **Separation of Concerns**: UI, services, and utilities are separated into distinct modules
2. **API-Driven**: All data operations go through the API service layer
3. **No Business Logic**: UI only handles presentation and user interaction
4. **Error Handling**: Comprehensive error handling at all layers
5. **Reusability**: Common components and utilities are shared across pages

## Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI Layer                    │
│  (app.py, pages/*) - Presentation and User Interaction   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Component Layer                          │
│  (components/*) - Reusable UI Components                 │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Service Layer                           │
│  (services/*) - API Communication                      │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Utility Layer                           │
│  (utils/*) - Configuration, Validation, Formatting     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Backend API                              │
│  (External) - Business Logic and Data Management         │
└──────────────────────────────────────────────────────────┘
```

## Directory Structure

### `/work/app.py`
Main entry point that:
- Configures Streamlit page settings
- Validates configuration
- Renders navigation
- Routes to appropriate pages
- Handles global errors

### `/work/pages/`
Individual page modules, each containing a `render()` function:
- `home.py`: Dashboard with summary cards
- `datasets.py`: Dataset upload and management
- `models.py`: Model browsing and details
- `experiments.py`: Experiment tracking with polling
- `evaluations.py`: Evaluation analysis and visualization
- `train_model.py`: Multi-step training wizard

### `/work/services/`
API service layer - one service per resource:
- `api_client.py`: Base HTTP client with error handling
- `dataset_service.py`: Dataset API calls
- `model_service.py`: Model API calls
- `experiment_service.py`: Experiment API calls
- `evaluation_service.py`: Evaluation API calls

### `/work/components/`
Reusable UI components:
- `navigation.py`: Sidebar navigation
- `status_badge.py`: Status indicator badges
- `loading_spinner.py`: Loading state indicators
- `error_message.py`: Error display components
- `empty_state.py`: Empty state messages

### `/work/utils/`
Utility functions:
- `config.py`: Configuration management (API URL, validation)
- `validators.py`: Form validation helpers
- `formatters.py`: Data formatting (dates, numbers, text)

## Data Flow

### User Action Flow

1. **User Interaction**: User clicks button/fills form in page component
2. **Validation**: Page validates input using validators
3. **Service Call**: Page calls appropriate service function
4. **API Request**: Service uses API client to make HTTP request
5. **Response Handling**: Service processes API response
6. **UI Update**: Page updates UI based on response
7. **Error Handling**: Errors are caught and displayed via error components

### Example: Upload Dataset

```
User fills form → datasets.py validates → dataset_service.upload_dataset() 
→ api_client.post() → Backend API → Response → Success/Error message
```

## State Management

Streamlit uses session state (`st.session_state`) for:
- Current page navigation
- Wizard step tracking
- Form data persistence
- Pagination state
- Selected items

## Error Handling Strategy

### Three-Layer Error Handling

1. **API Client Layer**: Catches network/HTTP errors, raises `APIError`
2. **Service Layer**: Propagates `APIError`, handles response parsing
3. **Page Layer**: Catches `APIError`, displays user-friendly messages

### Error Display

- No stack traces shown to users
- User-friendly error messages
- Retry buttons where applicable
- Clear indication of what went wrong

## Polling and Auto-Refresh

The Experiments page implements auto-refresh:
- Uses `st.rerun()` to refresh page
- Tracks last refresh time in session state
- Polls every 5-10 seconds when enabled
- Non-blocking UI updates

## Pagination

Pagination is implemented client-side:
- Data loaded from API
- Pagination state in session state
- Page controls (Previous/Next buttons)
- Handles up to 1,000 items per resource

## File Upload

File uploads handled via Streamlit's `st.file_uploader`:
- Validates file type (CSV, JSON, JSONL)
- Sends as multipart/form-data
- Shows upload progress
- Handles large files

## Multi-Step Wizard

The Train Model wizard uses:
- Session state for step tracking
- Step-by-step validation
- Progress indicator
- Summary view before launch
- Data persistence across steps

## Configuration Management

Configuration loaded from:
1. Environment variables (`.env` file)
2. Default values in `config.py`
3. Validation on app startup

## Performance Considerations

- Lazy loading: Data loaded only when needed
- Pagination: Large datasets split into pages
- Caching: Consider Streamlit caching for repeated API calls
- Polling: Configurable refresh intervals

## Security Assumptions (POC)

- No authentication/authorization
- API assumed trusted
- No input sanitization beyond validation
- No CSRF protection

## Future Enhancements

Potential improvements:
- Add Streamlit caching for API responses
- Implement WebSocket for real-time updates
- Add authentication/authorization
- Implement offline mode with local storage
- Add export functionality for reports
- Enhanced error recovery mechanisms
