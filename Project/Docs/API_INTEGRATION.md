# SLM Training Platform UI - API Integration Guide

## Overview

This document describes how the UI integrates with the backend API. All API communication is handled through the service layer in `work/services/`.

## API Base URL Configuration

The API base URL is configured via the `API_BASE_URL` environment variable in the `.env` file:

```env
API_BASE_URL=http://localhost:8000
```

## API Client

The base API client (`services/api_client.py`) provides:

- HTTP GET/POST requests
- File download support
- Error handling and retry logic
- JSON request/response handling
- Timeout handling (30 seconds default)

### Error Handling

The API client raises `APIError` exceptions for:
- HTTP errors (4xx, 5xx)
- Network errors (connection failures, timeouts)
- Invalid responses

All errors are caught and displayed as user-friendly messages in the UI.

## API Endpoints

### Dataset APIs

#### Upload Dataset
- **Endpoint**: `POST /datasets/upload`
- **Service**: `dataset_service.upload_dataset()`
- **Request**: Multipart form data with file, name, description, dataset_type
- **Response**: Dataset object with id, name, dataset_type, row_count, upload_date

#### Get All Datasets
- **Endpoint**: `GET /datasets`
- **Service**: `dataset_service.get_datasets()`
- **Response**: List of dataset objects

#### Download Dataset
- **Endpoint**: `GET /datasets/{id}/download`
- **Service**: `dataset_service.download_dataset()`
- **Response**: File content (bytes)

### Model APIs

#### Get All Models
- **Endpoint**: `GET /models`
- **Service**: `model_service.get_models()`
- **Query Params**: `model_type` (optional: "base" or "fine_tuned")
- **Response**: List of model objects

#### Get Model by ID
- **Endpoint**: `GET /models/{id}`
- **Service**: `model_service.get_model()`
- **Response**: Model object with full details

### Experiment APIs

#### Create Experiment
- **Endpoint**: `POST /experiments`
- **Service**: `experiment_service.create_experiment()`
- **Request Body**: JSON with name, description, goal, base_model_id, training_dataset_id, eval_dataset_id, training_config
- **Response**: Experiment object

#### Get All Experiments
- **Endpoint**: `GET /experiments`
- **Service**: `experiment_service.get_experiments()`
- **Response**: List of experiment objects

#### Get Experiment by ID
- **Endpoint**: `GET /experiments/{id}`
- **Service**: `experiment_service.get_experiment()`
- **Response**: Experiment object with full details

### Evaluation APIs

#### Get All Evaluations
- **Endpoint**: `GET /evaluations`
- **Service**: `evaluation_service.get_evaluations()`
- **Query Params**: `experiment_id` (optional)
- **Response**: List of evaluation objects

#### Get Evaluation by ID
- **Endpoint**: `GET /evaluations/{id}`
- **Service**: `evaluation_service.get_evaluation()`
- **Response**: Evaluation object with metrics, loss_curve, training_statistics

## Response Format Handling

The service layer handles various response formats:

- Direct list: `[{...}, {...}]`
- Wrapped in object: `{"items": [{...}, {...}]}`
- Named array: `{"datasets": [{...}, {...}]}`

All services normalize responses to return a consistent list format.

## Error Response Format

API errors should follow this format:

```json
{
  "detail": "Error message here"
}
```

Or:

```json
{
  "message": "Error message here"
}
```

The API client extracts the error message from these fields.

## Status Codes

- `200 OK`: Successful GET request
- `201 Created`: Successful POST request (creation)
- `400 Bad Request`: Invalid request data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
- Connection errors: Network/timeout issues

## Polling Behavior

The Experiments page polls for status updates every 5-10 seconds when auto-refresh is enabled. This is handled client-side using Streamlit's `st.rerun()`.

## File Upload

File uploads use multipart/form-data format:

```
file: (file content)
name: string
description: string
dataset_type: "training" | "evaluation"
```

Supported file types: CSV, JSON, JSONL

## Testing API Integration

To test API integration:

1. Ensure backend API is running
2. Check API_BASE_URL in `.env` file
3. Navigate to Home page - should load summary cards
4. Try uploading a dataset
5. Check browser console for any errors

## Mock API (For Testing)

If backend is not available, you can create mock responses by modifying the service layer to return sample data instead of making API calls.
