# Custom SLM Training Platform  
## Backend API Guide  
**Document Type:** API Specification  
**Scope:** Backend APIs only  
**Consumers:** Streamlit UI  
**Style:** REST, JSON, async training

---

## 1. Purpose of This API Guide

This document defines the **official contract** between:
- Streamlit UI (client)
- Backend service (API)
- External training infrastructure

The backend:
- Manages metadata
- Triggers training jobs
- Tracks experiments and evaluations

The backend **does NOT**:
- Perform model training logic itself
- Serve models for inference
- Deploy models

---

## 2. API Design Principles (Project-Specific)

1. **Stateless APIs**
   - Every request is independent
2. **Async training**
   - Training is never blocking
3. **Database is the source of truth**
4. **Blob storage stores files**
5. **Clear lifecycle states**
6. **UI polls, backend updates**

---

## 3. Base Assumptions

- Authentication is skipped (POC)
- JSON is used everywhere
- HTTP status codes are respected
- Backend uses:
  - FastAPI / Flask (recommended)
  - PostgreSQL / Azure SQL
  - Azure Blob Storage
  - External GPU training environment

---

## 4. Status & Lifecycle Definitions

### Experiment Status
| Status | Meaning |
|-----|-------|
| created | Experiment created, not started |
| running | Training in progress |
| completed | Training finished successfully |
| failed | Training failed |
| cancelled | User/system cancelled |

---

## 5. API Endpoints Overview

### Dataset APIs
- `POST /datasets/upload`
- `GET /datasets`
- `GET /datasets/{id}/download`

### Model APIs
- `GET /models`
- `GET /models/{id}`

### Experiment APIs
- `POST /experiments`
- `GET /experiments`
- `GET /experiments/{id}`

### Evaluation APIs
- `GET /evaluations`
- `GET /evaluations/{id}`

---

## 6. Dataset APIs

---

### 6.1 Upload Dataset

**Endpoint**  
`POST /datasets/upload`

**Purpose**  
Upload training or evaluation dataset.

**Request (multipart/form-data)**  
- file: CSV / JSON / JSONL
- name: string
- description: string
- dataset_type: `training` | `evaluation`

**Response (201)**  
```json
{
  "dataset_id": "ds_123",
  "name": "support_data_v1",
  "dataset_type": "training",
  "row_count": 2500,
  "upload_date": "2026-01-11"
}
