# Custom SLM Training Platform  
## UI Product Requirements Document (PRD)  
**Technology:** Streamlit  
**Document Type:** UI PRD  
**Scope:** Frontend only (No backend implementation)

---

## 1. Product Overview

### 1.1 Purpose
Build a **web-based UI** that allows users to:
- Upload datasets
- Select base models
- Trigger SLM training jobs
- Track experiments
- View evaluation results

This UI acts as a **control plane** for managing SLM training workflows.  
All training logic is handled externally via APIs.

---

### 1.2 Target Users
- ML Engineers
- Applied AI Engineers
- Internal platform users
- Data Scientists (non-infra focused)

---

### 1.3 Non-Goals
The UI **will NOT**:
- Perform model training
- Run GPU workloads
- Execute long-running jobs
- Deploy or serve models
- Validate data quality deeply

---

## 2. User Flow (High-Level)

1. User opens the application
2. Lands on Home / Dashboard
3. Navigates via sidebar to:
   - Datasets
   - Models
   - Experiments
   - Evaluations
4. Can initiate training via “Train Model” wizard
5. Can monitor experiment status
6. Can view metrics and loss curves

---

## 3. Global UI Requirements

### 3.1 Navigation
- Left sidebar navigation
- Persistent across all pages

**Navigation Items:**
- Home
- Datasets
- Models
- Experiments
- Evaluations
- Train Model

---

### 3.2 Global States
All pages must handle:
- Loading state (spinner)
- Empty state (no data)
- Error state (API failure)
- Success state (confirmation)

---

### 3.3 UI Principles
- Simple
- Minimal
- Readable tables
- Clear call-to-action buttons
- No nested complexity

---

## 4. Page-Level Requirements

---

## 4.1 Home / Dashboard Page

### Purpose
Provide a quick overview of the system status.

### Components
- Summary cards:
  - Total datasets
  - Total models
  - Total experiments
- Recent experiments table (last 5)

### Actions
- Navigate to Train Model

### API Dependencies
- `GET /datasets`
- `GET /models`
- `GET /experiments`

---

## 4.2 Datasets Page

### Purpose
Manage training and evaluation datasets.

### Components
1. Dataset upload form
   - Dataset name
   - Description
   - Dataset type (Training / Evaluation)
   - File upload (CSV / JSON / JSONL)
2. Dataset table
   - Name
   - Type
   - Row count
   - Upload date
   - Actions: Download

### User Actions
- Upload dataset
- View dataset list
- Download dataset

### API Dependencies
- `POST /datasets/upload`
- `GET /datasets`
- `GET /datasets/{id}/download`

---

## 4.3 Models Page

### Purpose
Browse available base models and trained models.

### Components
1. Models table
   - Model name
   - Model type (Base / Fine-tuned)
   - Version
   - Architecture
   - Parameters count
   - Created date
   - Is latest version
2. Model detail drawer (on click)
   - Description
   - Metadata
   - Linked evaluations

### User Actions
- View model details
- Filter by model type

### API Dependencies
- `GET /models`
- `GET /models/{id}`

---

## 4.4 Experiments Page

### Purpose
Track training runs and their status.

### Components
1. Experiments table
   - Experiment name
   - Status (running / completed / failed / cancelled)
   - Base model
   - Dataset
   - Created date
   - Actions: View details
2. Experiment detail view
   - Goal
   - Training config
   - Status timeline
   - Link to resulting model
   - Link to evaluations

### User Actions
- Monitor experiment status
- Navigate to evaluation results

### API Dependencies
- `GET /experiments`
- `GET /experiments/{id}`

---

## 4.5 Evaluations Page

### Purpose
Analyze model performance.

### Components
1. Evaluation selector
   - Experiment
   - Model
   - Evaluation dataset
2. Metrics panel
   - Accuracy
   - F1
   - Perplexity
3. Loss curve visualization
4. Training statistics table

### User Actions
- Compare evaluation runs
- View metrics

### API Dependencies
- `GET /evaluations`
- `GET /evaluations/{id}`

---

## 4.6 Train Model Wizard Page

### Purpose
Guide user through training configuration.

### Steps

#### Step 1: Experiment Details
- Experiment name
- Description
- Goal

#### Step 2: Base Model Selection
- Dropdown of base models

#### Step 3: Training Dataset Selection
- Dropdown of training datasets

#### Step 4: Evaluation Dataset Selection
- Dropdown of eval datasets

#### Step 5: Training Configuration
- Learning rate
- Epochs
- Batch size

#### Step 6: Review & Launch
- Summary view
- Launch button

### User Actions
- Configure training
- Submit training request

### API Dependencies
- `POST /experiments`

---

## 5. Error Handling Requirements

### API Failure
- Show readable error message
- No stack traces
- Retry option where applicable

### Validation Errors
- Inline field-level errors
- Disable submit until valid

---

## 6. Loading & Polling Behavior

- Experiments page polls status every 5–10 seconds
- No blocking UI
- Spinner during refresh

---

## 7. Performance Constraints

- UI must handle up to:
  - 1,000 datasets
  - 1,000 experiments
- Pagination required for tables

---

## 8. Security Assumptions (POC)

- No user roles
- No access control
- API assumed trusted

---

## 9. Deliverables

- Fully functional Streamlit UI
- Clean page separation
- API calls abstracted into service layer
- No business logic in UI

---

## 10. Acceptance Criteria

- User can complete full training flow without errors
- All pages load independently
- No training logic exists in UI
- UI is API-driven only

---

## END OF DOCUMENT
