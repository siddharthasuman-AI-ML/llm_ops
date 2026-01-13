# SLM Training Platform – POC

## Overview

This project is a **Proof of Concept (POC) web platform** designed to manage the **end-to-end lifecycle of Small Language Model (SLM) training** in a structured, traceable, and enterprise-friendly manner.

The platform acts as a **control plane** for model training activities, abstracting away infrastructure complexity while providing clear visibility into datasets, training runs, experiments, models, and evaluations.

The primary goal is **clarity, traceability, and operational correctness**, not infrastructure management.

---

## Core Objectives

* Enable structured upload and management of training and evaluation datasets
* Provide a controlled workflow to launch model training runs
* Track experiments and their outcomes
* Maintain a versioned model registry with full lineage
* Centralize evaluation metrics and results
* Ensure all artifacts are linkable and auditable

---

## High-Level Architecture

### Frontend

* Web UI (POC-friendly, table-driven)
* Acts as the **control layer** only
* No direct infrastructure exposure

### Backend

* API-driven orchestration layer
* Handles training job submission, status tracking, and metadata persistence

### Storage

* Database: Source of truth for metadata (datasets, runs, models, evaluations)
* Blob/Object Storage: Stores datasets, model artifacts, logs

### Training Infrastructure

* Treated as a **black box**
* Triggered via APIs
* No direct UI-level controls

---

## Application Navigation

The platform is organized into five primary sections:

1. Datasets
2. Training Runs
3. Experiments
4. Models
5. Evaluations

Navigation is global and consistent across all pages.

---

## Datasets

### Purpose

Manage datasets used for training and evaluation.

### Dataset Types

* Text
* Images
* Tabular

### Dataset Usage

* Training
* Evaluation

### Dataset Status

* In Progress (upload/processing)
* Uploaded / Processed
* Error

### Dataset Capabilities

* Upload new datasets
* View dataset metadata
* Preview sample rows (when available)
* Download datasets
* Retry upload for failed datasets
* Delete datasets

### Dataset Metadata

* Name
* Row count
* Type
* Usage
* Status
* Size
* Added date
* Owner (optional)

All datasets are presented in a **table-first view**.

---

## Training Runs

### Purpose

Provide a **guided, controlled workflow** to initiate model training.

### Training Run Creation

Training runs are created exclusively via a **step-by-step wizard**:

1. Metadata
2. Data Selection
3. Hyperparameters
4. Confirmation

### Metadata

* Run name
* Base model selection
* Primary dataset selection

### Data Selection

* Training dataset
* Evaluation dataset

### Hyperparameters

* Epochs
* Learning rate
* Batch size

### Confirmation

* Read-only summary of all inputs
* Explicit launch action

This ensures consistency, repeatability, and auditability.

---

## Experiments

### Purpose

Track individual training executions and their outcomes.

### Experiment Characteristics

* One experiment corresponds to one training execution
* Experiments are **read-only artifacts**

### Experiment Metadata

* Experiment ID
* Status (running, completed, failed)
* Base model
* Dataset used
* Start time
* Completion time
* Resulting model

Experiments act as the **operational backbone** connecting datasets, training runs, models, and evaluations.

---

## Models

### Purpose

Serve as a **centralized model registry** with versioning and lineage.

### Model Types

* Base models
* Fine-tuned models

### Model Naming

Models follow a structured naming convention:

```
<model_family>-v<version>
```

### Model Capabilities

* View model metadata
* Identify latest versions
* Navigate to detailed model cards

### Model Metadata

* Model ID
* Family name
* Version and version number
* Model type
* Base model reference
* Creation date
* Latest version indicator

All models are displayed in a table with column-level sorting.

---

## Model Card

### Purpose

Provide a **single source of truth** for a model.

### Model Card Structure

#### Model Metadata

* Model identifiers
* Versioning information
* Architecture details
* Parameter count
* Parent and base model references
* Additional metadata

#### Training Details

* Base model used
* Training dataset used
* Evaluation dataset used
* Training configuration
* Training objective
* Related experiments
* Related evaluations
* Model lineage visualization

The model card ensures full traceability from dataset to final model artifact.

---

## Evaluations

### Purpose

Centralize evaluation results and metrics.

### Evaluation Capabilities

* View evaluation runs
* Filter by model and date
* Inspect metrics and loss curves

### Evaluation Metadata

* Evaluation ID
* Model evaluated
* Dataset used
* Evaluation date
* Metrics summary

Evaluations are strictly read-only and linked back to experiments and models.

---

## Design Principles

* Table-first UI for clarity and scalability
* Wizard-driven creation flows
* Explicit enums and controlled states
* No inline editing of critical artifacts
* Strong cross-linking between entities
* Read-heavy, write-controlled system
* POC scope with enterprise extensibility

---

## Scope and Limitations

* Authentication and RBAC are out of scope for the POC
* Advanced infrastructure controls are intentionally excluded
* Assumes small-to-medium datasets
* Focused on correctness and traceability over visual polish

---

## Summary

This platform provides a **structured, auditable, and extensible foundation** for managing the SLM training lifecycle. It enables teams to move from dataset ingestion to model evaluation with full visibility, while keeping complexity controlled and responsibilities clearly separated.
