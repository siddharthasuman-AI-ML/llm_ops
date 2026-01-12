# Custom SLM Training Platform  
## Database Schema (SQL)

---

## 1. datasets

```sql
CREATE TABLE datasets (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    dataset_type TEXT CHECK (dataset_type IN ('training', 'evaluation')),
    file_path TEXT NOT NULL,
    row_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

============================================================================================
SQL
CREATE TABLE models (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    model_type TEXT CHECK (model_type IN ('base', 'fine_tuned')),
    base_model_id UUID,
    version TEXT,
    parameters_count BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


==========================================================================

SQL
CREATE TABLE experiments (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    goal TEXT,
    base_model_id UUID REFERENCES models(id),
    training_dataset_id UUID REFERENCES datasets(id),
    eval_dataset_id UUID REFERENCES datasets(id),
    status TEXT,
    training_config JSONB,
    resulting_model_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
========================================================================
CREATE TABLE evaluations (
    id UUID PRIMARY KEY,
    experiment_id UUID REFERENCES experiments(id),
    metrics JSONB,
    loss_curve JSONB,
    training_statistics JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
========================================================================

5. Key Design Notes

Metadata only in DB

Files stored in blob storage

JSONB used for flexibility

Full lineage preserved