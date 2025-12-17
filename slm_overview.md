# Technical Report: LLMOps Pipeline for Domain-Specific SLM Customization

## 1. Executive Summary

The project goal is to develop a robust, automated, and continuous pipeline for fine-tuning a base Small Language Model (SLM) (e.g., Meta Llama 3.1 8B Instruct) to specialize in automotive terminology, enabling accurate diagnostics and Q&A. This solution leverages AWS services for a complete **LLMOps lifecycle**, ensuring high data quality, cost-efficient training via **LoRA**, automated evaluation, and seamless, serverless deployment via **Amazon Bedrock**. The entire process is orchestrated by **Amazon SageMaker Pipelines**.

---

## 2. Core Architecture & Services

The architecture is composed of four primary phases managed by a single **SageMaker Pipeline** definition.

| AWS Service | Primary Role in LLMOps | Key Functionality |
| :--- | :--- | :--- |
| **Amazon SageMaker Pipelines** | **Orchestration / LLMOps** | Defines the end-to-end CI/CD workflow, managing dependency graph and parameter passing between steps.  |
| **Amazon S3** | **Data Management** | Securely stores raw data, processed data, model artifacts (LoRA adapter weights), and logs. |
| **Amazon SageMaker** | **ML Computing** | Provides managed compute for **Processing Jobs** (data prep), **Training Jobs** (LoRA fine-tuning), and **Evaluation Steps**. |
| **Amazon Bedrock** | **Inference & Consumption** | Handles the final, serverless hosting and scaling of the customized SLM via **Custom Model Import**. |
| **Amazon EventBridge** | **Automation Trigger** | Detects events (e.g., new data in S3) and automatically starts the SageMaker Pipeline execution. |
| **AWS Lambda (Optional)** | **Automation Logic / Glue** | Used for pre-pipeline data validation, parameter setting, and post-pipeline alerting/notification. |

---

## 3. End-to-End Pipeline Workflow (E2E Steps)

The pipeline is designed for continuous execution upon new data arrival or on a fixed schedule.

### Phase A: Data Ingestion & Preprocessing

This phase focuses on ensuring the highest quality training data, crucial for effective domain specialization.

| Service/Component | Task | Technical Detail |
| :--- | :--- | :--- |
| **Data Source (S3)** | **Ingestion Trigger** | New `Automotive_NER` or proprietary diagnostic data is uploaded to a designated S3 prefix (e.g., `s3://automotive-data/raw/`). |
| **Amazon EventBridge** | **Pipeline Initiation** | An EventBridge Rule monitors the S3 `PutObject` event, targeting and starting the SageMaker Pipeline. |
| **(Optional) AWS Lambda** | **Pre-Processing Logic** | Invoked by EventBridge. Validates input schema/size and dynamically sets run-time parameters for the pipeline (e.g., `training_data_path`). |
| **SageMaker Processing Job** | **Data Cleansing & Subsetting** | Runs on a specified instance (e.g., `ml.m5.4xlarge`). Key tasks include: **Text Preprocessing**, **TF-IDF Vectorization** for feature importance, and creating a balanced training subset (Top 6k important words + Bottom 6k rare words). |
| **S3** | **Artifact Output** | Stores the finalized, processed Q&A formatted dataset for training (e.g., `s3://automotive-data/processed/`). |

### Phase B: Model Training & Artifact Generation

This phase executes the domain-specific knowledge transfer.

| Service/Component | Task | Technical Detail |
| :--- | :--- | :--- |
| **SageMaker Training Job** | **LoRA Fine-tuning** | Runs on a GPU-accelerated instance (e.g., `ml.g5.12xlarge`). Uses the **Hugging Face container** and **PEFT (LoRA)** to efficiently update the Llama 3.1 8B parameters. |
| **S3** | **Model Artifacts** | Stores the resulting **LoRA adapter weights** (which are much smaller than the full model), ready to be applied to the base model. |

### Phase C: Model Evaluation and Governance

This phase is the quality gate, essential for maintaining reliability and preventing the deployment of degraded models.

| Service/Component | Task | Technical Detail |
| :--- | :--- | :--- |
| **SageMaker Evaluation Step**| **Factual Accuracy Testing** | Runs inference against a test set. Key custom metrics: **Domain-Specific Accuracy**, **Vocabulary Richness Score** (usage of DTCs), and **Hallucination Rate**. |
| **SageMaker Condition Step**| **Quality Gate** | Implements the business logic check: `AccuracyMetric > 0.95`. If the condition fails, the pipeline terminates, and a failure notification is triggered. |
| **SageMaker Model Registry**| **Version Control & Approval** | The approved model and its metrics are formally logged, creating a traceable model lineage and requiring formal approval for production. |

### Phase D: Deployment and Monitoring

This phase moves the approved model into production for inference, prioritizing scalability and ease of use.

| Service/Component | Task | Technical Detail |
| :--- | :--- | :--- |
| **Amazon Bedrock** | **Custom Model Import** | The registered LoRA adapter weights and the base Llama 3.1 model ID are combined during the import, resulting in a managed, custom model endpoint. |
| **Amazon Bedrock** | **Inference Endpoint** | Provides a highly scalable, serverless endpoint via the `InvokeModel` API, abstracting GPU management. |
| **Application Layer** | **Consumption** | External applications call the Bedrock endpoint to leverage the specialized Q&A capability. |
| **Amazon CloudWatch** | **Monitoring & Alerting** | Monitors inference metrics (latency, throughput, error rates) and sets up alarms to detect **Model Drift** (performance degradation). |
| **(Optional) AWS Lambda** | **Remediation / Rollback** | CloudWatch alarms can trigger a Lambda function to initiate an automated rollback to the last known good model version in Bedrock, or send an alert via **Amazon SNS**. |

---

## 4. Key Technical Decisions & Justifications

| Decision | Justification |
| :--- | :--- |
| **SLM (Llama 3.1 8B) over LLM** | **Cost & Efficiency:** Significantly lower GPU costs for training and inference. Ideal for a **narrow, domain-specific** task like automotive diagnostics. |
| **LoRA Fine-tuning** | **Speed & Cost:** Drastically reduces training time and memory footprint compared to full fine-tuning, accelerating the iteration cycle required for LLMOps. |
| **SageMaker Pipelines** | **Automation & Governance:** Provides the necessary structure for automated CI/CD and enforces quality gates (Condition Step) before production deployment. |
| **Bedrock Deployment** | **Serverless Scalability:** Eliminates the operational overhead of managing GPU endpoints, autoscaling, and patching. Offers simple, consumption-based pricing and a unified API for enterprise use. |

| **TF-IDF Subsetting** | **Data Quality:** Ensures the model is trained on the most **semantically rich** (jargon) and **representative** data, maximizing knowledge transfer while minimizing compute time. |


import csv
import json
from pathlib import Path

# Input / Output paths
input_csv = Path("data/raw/svg_color.csv")
output_json = Path("data/svg/final_dataset_color.json")

output_json.parent.mkdir(parents=True, exist_ok=True)

dataset = []

with open(input_csv, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        dataset.append({
            "id": idx,
            "question": row["question"],
            "answer": row["answer"],
            "vg_code": row["svg"],
            "vg_format": "svg",
            "meta": {
                "type": "color"
            }
        })

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2)

print(f"Saved {len(dataset)} samples to {output_json}")
