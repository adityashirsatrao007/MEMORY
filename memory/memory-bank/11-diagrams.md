## 📊 Diagrams, Architecture & Documentation — Mandatory Rules

### Core Rule
NEVER use AI-generated images for diagrams. ALWAYS plot/render them programmatically using code.
All diagram files MUST be saved to `docs/images/` with descriptive filenames.
Every project README MUST include at minimum: architecture diagram + data/ML flow diagram.

---

### Tool Selection — Agent Picks Best Tool Per Diagram Type

| Diagram Type | Tool | Why | Output |
|-------------|------|-----|--------|
| System/Cloud Architecture | **`diagrams` (mingrammer)** | Python, 1000+ cloud icons (AWS/GCP/Azure/K8s), code → PNG | PNG |
| Flowcharts, Sequences, ERDs | **D2 (`d2`)** | Text → PNG, version-controllable, dark theme | PNG |
| ML Pipeline / Data Flow | **`diagrams` + custom nodes** | Full pipeline visual with icons | PNG |
| Beautiful modern diagrams | **D2** | Best layout engine, cleanest output | PNG/SVG |
| Statistical plots / metrics | **Plotly + kaleido** | Interactive → high-res PNG export | PNG |
| Training curves / EDA | **Matplotlib + seaborn** | Scientific quality, customizable | PNG |
| Network/Graph structures | **NetworkX + matplotlib** | Node-link diagrams for any graph | PNG |
| Dependency trees / DAGs | **Graphviz (`dot`)** | Standard for dependency graphs | PNG |

---

### DIAGRAM DECISION TREE

```
What are you documenting?

Web/Mobile App?
  → System components + APIs    → diagrams (mingrammer) → docs/images/architecture.png
  → User flow / screen flow     → D2 flowchart     → docs/images/userflow.png
  → Database schema (ERD)       → D2 ERD     → docs/images/erd.png
  → API sequence                → D2 sequence→ docs/images/api-sequence.png

ML/DL Project?
  → Full ML pipeline            → diagrams (mingrammer) → docs/images/ml-pipeline.png
  → Training loss/accuracy      → Matplotlib/Plotly     → docs/images/training-curves.png
  → Model architecture (layers) → Matplotlib custom     → docs/images/model-architecture.png
  → Data flow                   → D2 flowchart     → docs/images/data-flow.png
  → Confusion matrix            → Seaborn heatmap       → docs/images/confusion-matrix.png
  → Feature importance          → Plotly bar chart      → docs/images/feature-importance.png

Cloud/DevOps?
  → Infrastructure              → diagrams (mingrammer) → docs/images/infrastructure.png
  → CI/CD pipeline              → D2 flowchart     → docs/images/cicd-pipeline.png
  → Deployment topology         → D2                    → docs/images/deployment.png
```

---

### Code Templates — Agent Uses These Directly

To generate diagrams, copy the templates from the following paths and customize them for the project:
- **System Architecture (mingrammer):** Copy `/home/aditya/bin/templates/diagrams/generate_architecture.py` to `docs/generate_architecture.py`
- **Flowchart / Sequence / ERD (D2):** Copy `/home/aditya/bin/templates/diagrams/userflow.d2` to `docs/diagrams/userflow.d2` (and run `d2 --theme=200 docs/diagrams/userflow.d2 docs/images/userflow.png` to render)
- **ML Pipeline Diagram (matplotlib):** Copy `/home/aditya/bin/templates/diagrams/generate_ml_pipeline.py` to `docs/generate_ml_pipeline.py`
- **Training Curves (matplotlib):** Copy `/home/aditya/bin/templates/diagrams/save_training_curves.py` to `docs/save_training_curves.py`
- **Confusion Matrix (seaborn):** Copy `/home/aditya/bin/templates/diagrams/save_confusion_matrix.py` to `docs/save_confusion_matrix.py`

### Matplotlib Visual Quality Standards
When plotting any training metrics or results manually, always import the standard styles. Ensure you set the following visual parameters for clinical/high-end UI compliance:
- Figure background: `#1C1C1E` (Apple dark)
- Axes background: `#2C2C2E`
- Font size: 12, Titles: 14 bold
- Line width: 2.5
- Save DPI: 200 (high-res PNG)

---

### File Naming Convention
```
docs/images/
├── architecture.png          ← system architecture (diagrams library)
├── ml-pipeline.png           ← ML data/model flow
├── userflow.png              ← user journey flowchart (mermaid)
├── erd.png                   ← database schema (mermaid)
├── api-sequence.png          ← API call sequence (mermaid)
├── training-curves.png       ← loss + accuracy over epochs
├── confusion-matrix.png      ← classification results
├── feature-importance.png    ← top features bar chart
├── deployment.png            ← infrastructure (diagrams/D2)
└── cicd-pipeline.png         ← CI/CD flow (mermaid)
```

### README Integration Template
```markdown
## Architecture
![System Architecture](docs/images/architecture.png)

## Data Flow
![ML Pipeline](docs/images/ml-pipeline.png)

## Training Results
![Training Curves](docs/images/training-curves.png)
```

### Generate All Diagrams Command
Every project Makefile gets this target:
```makefile
diagrams:  ## Generate all architecture and flow diagrams
	@mkdir -p docs/images docs/diagrams
	@python docs/generate_architecture.py
	@python docs/generate_ml_pipeline.py
	@find docs/diagrams -name "*.mmd" -exec sh -c \
	  'mmdc -i {} -o docs/images/$$(basename {} .mmd).png -t dark -w 2400' \;
	@echo "✅ All diagrams generated in docs/images/"

---

