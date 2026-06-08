# ML/DL Engineering — Autonomous Workflow

> Extracted from `GEMINI.md`. See `memory/modules/02-cli-tools.md` for ML tool installation, `memory/modules/04-security.md` for API key security, `memory/modules/01-core-rules.md` for production standards.

---

## Python Environment & Credentials
- **Development:** Docker-based dev environment (devcontainer.json + docker-compose)
- **CI/CD:** GitLab CI / GitHub Actions builds and pushes container images to private registry
- **Production:** Containers run on Kubernetes (EKS/GKE/AKS) with resource limits and autoscaling
- **GPU:** Production multi-node GPU cluster (A100/H100), managed by Kubernetes + FSDP

### All Configured API Keys (Vault-Managed)
| Service | Env Var | Source |
|---------|---------|--------|
| HuggingFace | `HF_TOKEN` | Vault `secret/ml/huggingface` |
| Kaggle | `KAGGLE_API_TOKEN` | Vault `secret/ml/kaggle` |
| Weights & Biases | `WANDB_API_KEY` | Vault `secret/ml/wandb` |
| Roboflow | `ROBOFLOW_API_KEY` | Vault `secret/ml/roboflow` |

### Using Each Service in Code
```python
import os
import hvac  # HashiCorp Vault client

# All secrets are injected via Kubernetes secrets or Vault sidecar
# No secrets stored in bashrc, netrc, or local files

# HuggingFace
from huggingface_hub import login
login(token=os.environ['HF_TOKEN'])

# Kaggle - KAGGLE_API_TOKEN injected via K8s secret volume mount

# wandb
import wandb
wandb.init(project="my-project")

# Roboflow
from roboflow import Roboflow
rf = Roboflow(api_key=os.environ['ROBOFLOW_API_KEY'])
```

### Agent Picks Models Automatically (Transfer Learning First)
Never train from scratch. Always:
1. Search HuggingFace Hub for best pre-trained model for the task
2. Load with `from_pretrained()` — cached in S3/GCS via HuggingFace Hub cache mount
3. Fine-tune with FSDP/DeepSpeed sharding across multi-node GPU cluster
4. Evaluate with `evaluate` library metrics, log to MLflow

---

### 🧠 MASTER DECISION TREE — Agent Uses This For Every ML Task

#### STEP 1: Feature Store (Feast/Tecton) Instead of Raw Data Dirs
Define features in a centralized registry before any training begins:
```python
# feature_store/feature_definitions.py
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String

user = Entity(name="user_id", value_type=Int64)

user_stats = FeatureView(
    name="user_statistics",
    entities=["user_id"],
    ttl=timedelta(days=7),
    schema=[
        Field(name="avg_session_duration", dtype=Float32),
        Field(name="total_purchases", dtype=Int64),
    ],
    source=FileSource(path="s3://data-bucket/features/user_stats.parquet"),
)
```
- Online serving: Redis/Phoenix via Feast feature server at low latency
- Offline serving: Spark/batch query for training datasets
- Point-in-time joins prevent data leakage (automatic with Feast/Tecton)

#### STEP 2: Data Validation (Great Expectations) Before Training
```python
# great_expectations/suites/training_data_suite.json
{
  "expectations": [
    {"expectation_type": "expect_column_values_to_not_be_null", "kwargs": {"column": "label"}},
    {"expectation_type": "expect_column_values_to_be_between", "kwargs": {"column": "feature_1", "min_value": 0, "max_value": 1}},
    {"expectation_type": "expect_table_row_count_to_be_between", "kwargs": {"min_value": 1000, "max_value": 10_000_000}}
  ]
}
```
- Runs as a CI check before training is triggered
- Blocks pipeline on schema drift, nulls in critical columns, distribution shifts

#### STEP 3: Distributed Training (FSDP/DeepSpeed) on K8s
```yaml
# k8s/training-job.yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: trainer
    image: registry.example.com/trainer:latest
    resources:
      limits:
        nvidia.com/gpu: 8  # 8x A100
    env:
    - name: FSDP_SHARDING_STRATEGY
      value: "FULL_SHARD"
    - name: DEEPSPEED_ZERO_STAGE
      value: "3"
```
- FSDP shards parameters, gradients, optimizer states
- DeepSpeed ZeRO-3 for trillion-parameter model scaling
- Elastic training: pods can be preempted/rescheduled without losing progress
- Checkpointing to S3/GCS with resumability

#### STEP 4: Model Registry with Staging/Prod Gates (MLflow)
```yaml
# mlflow/model_registry.yaml
model_name: "transformer-ranker"
versions:
  - version: 12
    stage: "Staging"
    metrics: { "accuracy": 0.943, "latency_ms": 42 }
  - version: 11
    stage: "Production"
    metrics: { "accuracy": 0.938, "latency_ms": 39 }
promotion_rules:
  - accuracy >= current_production.accuracy
  - latency_ms <= 50
  - data_validation_passed: true
```
- Every model registered with full provenance: data version, code commit, hyperparameters
- Staging gate: automated canary deployment (5% traffic for 24h)
- Production gate: requires sign-off from validation checks + human approval
- Automatic rollback if production metrics degrade beyond threshold

#### STEP 5: Serving via Triton Inference Server + ONNX
```bash
# Export PyTorch → ONNX
torch.onnx.export(model, dummy_input, "model.onnx",
                  opset_version=17,
                  dynamic_axes={"input": {0: "batch_size"}})

# Triton config
name: "transformer_ranker"
backend: "onnxruntime"
max_batch_size: 256
dynamic_batching:
  preferred_batch_size: [4, 8, 16, 32]
instance_group:
  - count: 4
    kind: KIND_GPU
```
- Model parallelism via TensorRT-LLM or vLLM on Triton
- Dynamic batching maximizes GPU utilization
- Multiple model versions served simultaneously (blue/green)
- Concurrency and autoscaling via K8s HPA on gpu-utilization metric

#### STEP 6: Monitoring (Evidently + Prometheus + Grafana)
```yaml
# monitoring/evidently_service.yaml
data_drift:
  schedule: "hourly"
  alert_channels: ["slack", "pagerduty"]
  metrics:
    - model_accuracy < 0.90
    - data_drift_score > 0.15
    - prediction_distribution_jsd > 0.1
    - latency_p99 > 500ms
```
- Data drift: Evidently compares reference vs current feature distributions
- Model drift: Prediction distribution shifts, accuracy degradation
- Operational: Prometheus collects inference latency, throughput, error rates
- Dashboards: Grafana panels for model health, data quality, infrastructure

#### STEP 7: CI/CD (Data CI → Model CI → Deploy CI → Monitor)
```
Data CI ──► validation ──► trigger ──► Model CI ──► registry ──► Deploy CI ──► canary ──► Monitor
```
1. **Data CI:** Validate new data with Great Expectations, block if schema drift
2. **Model CI:** On data pass → train with FSDP on K8s → evaluate → register in MLflow
3. **Deploy CI:** On model register → build Triton model repo → deploy canary → shift traffic
4. **Monitor:** Evidently + Prometheus continuously monitor → alert on drift/regression
5. **Rollback:** Automated rollback to previous production model if metrics degrade

---

### Model Sources — Agent Picks Best Source Per Task
All pretrained models are pulled from HuggingFace Hub (cached via S3/GCS mount) or from the internal MLflow registry.

### Dataset Fetching — Agent Picks Best Source Automatically
Data is ingested via the feature store (Feast/Tecton) and validated with Great Expectations before entering the pipeline.

**Agent decision logic:**
- NLP task → HuggingFace Datasets → Feast offline store
- Vision task → Roboflow / Torchvision → Feast feature ingestion
- Competition data → Kaggle → Feast batch ingestion
- Classical ML → OpenML → Feast batch ingestion
- Production data → Feature store already has it versioned

### Experiment Tracking — Weights & Biases (Primary) + MLflow (Central Registry)
**Rule:** wandb for per-run experimentation and visualization. MLflow for the central model registry with staging/prod gates.

### Data Versioning — DVC
```bash
# Track large datasets without storing in git
dvc init
dvc add data/raw/dataset.csv
git add data/raw/dataset.csv.dvc .gitignore
git commit -m "add dataset"
dvc push  # push to remote storage (S3/GCS)
```

### Feature Engineering Pipeline (Replaces Ad-hoc Augmentation)
All feature transformations are defined in the feature store and applied consistently across training and serving:
```python
# features/transforms.py
from feast import FeatureView, Field
from feast.transforms import PythonTransform

@PythonTransform
def normalize_text_length(df):
    df["text_length_norm"] = df["text_length"] / df["text_length"].max()
    return df

text_features = FeatureView(
    name="text_features",
    entities=["document_id"],
    ttl=timedelta(days=30),
    schema=[Field(name="text_length_norm", dtype=Float32)],
    source=FileSource(path="s3://features/text_stats.parquet"),
    transforms=[normalize_text_length],
)
```

### ML Project Structure (Auto-Created by Agent)
```
project/
├── .github/workflows/    ← CI/CD pipelines (Data CI, Model CI, Deploy CI, Monitor)
├── infra/                ← K8s manifests, Helm charts, Terraform
├── features/             ← Feature definitions (Feast/Tecton)
├── data/                 ← DVC-tracked, versioned datasets
├── models/               ← MLflow registry configs, Triton model repo
├── src/
│   ├── data/             ← Great Expectations validation suites
│   ├── features/         ← Feature engineering transforms
│   ├── training/         ← FSDP training scripts
│   └── serving/          ← Triton model configs, ONNX export
├── monitoring/           ← Evidently profiles, Grafana dashboards
├── Dockerfile
├── docker-compose.yml    ← Local dev with MinIO + Feast + MLflow
└── Makefile
```

### Kaggle Competition Workflow (Full Automation)
1. `kaggle competitions download -c <name> -p data/raw/`
2. EDA notebook auto-generated
3. Baseline model from HuggingFace
4. Training with MLflow tracking
5. `kaggle competitions submit -c <name> -f submission.csv -m "baseline"`

---

## Diagrams, Architecture & Documentation — Mandatory Rules

### Core Rule
NEVER use AI-generated images for diagrams. ALWAYS plot/render them programmatically using code.
All diagram files MUST be saved to `docs/images/` with descriptive filenames.

### Tool Selection — Agent Picks Best Tool Per Diagram Type
| Diagram Type | Tool | Output |
|-------------|------|--------|
| System/Cloud Architecture | `diagrams` (mingrammer) | PNG |
| Flowcharts, Sequences, ERDs | D2 (`d2`) | PNG |
| ML Pipeline / Data Flow | `diagrams` + custom nodes | PNG |
| Training curves / EDA | Matplotlib + seaborn | PNG |
| Statistical plots / metrics | Plotly + kaleido | PNG |

### Matplotlib Visual Quality Standards
- Figure background: `#1C1C1E` (Apple dark)
- Axes background: `#2C2C2E`
- Font size: 12, Titles: 14 bold
- Line width: 2.5
- Save DPI: 200 (high-res PNG)

### Generate All Diagrams Command
```makefile
diagrams:  ## Generate all architecture and flow diagrams
	@mkdir -p docs/images docs/diagrams
	@python docs/generate_architecture.py
	@python docs/generate_ml_pipeline.py
```
