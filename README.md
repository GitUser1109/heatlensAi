# HeatLens AI — Urban Microclimate Intelligence Platform
**CSE (AIML) × Environmental Studies Decision Support System**

A local-first, full-stack environmental analytics system combining an interactive web dashboard, a high-throughput FastAPI backend, and an explainable Random Forest regression model with tree-ensemble uncertainty estimation and what-if cooling intervention simulation.

---

## ⚠️ Important Scientific Data Integrity Notice

**The default repository uses reproducible synthetic microclimate demonstration data.**  
The model is trained to learn an illustrative *relative heat-risk index (0–100)* from simulated environmental variables. It demonstrates an end-to-end machine learning engineering workflow, spatial exploration, and policy simulation. **It does NOT represent measured ground temperatures or validated municipal forecasts for Mumbai.**

To transition this educational prototype into peer-reviewed empirical research, refer to the documented satellite data integration roadmap in [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md).

---

## Key System Features

- **Professional Environmental Analytics Dashboard:** Modern dark/light glassmorphic UI with Google Fonts (Outfit & Plus Jakarta Sans), fluid responsive split-grid layouts, and KPI diagnostic cards.
- **Defensible Uncertainty Quantification:** Unlike black-box point estimates, computes epistemic prediction variance ($\pm 1.96\sigma$) across all 220 individual decision tree estimators in the ensemble.
- **Statistical Benchmark Comparison:** Evaluates the Random Forest regressor against both a naive Dummy Mean baseline (11.31 MAE) and a Ridge linear model (3.82 MAE), achieving **3.61 MAE** and **0.871 $R^2$** on held-out test data.
- **In-Memory Cached Inference:** Model bundle loaded into memory once at server startup (lifespan cache), reducing inference latency to sub-3ms and eliminating repeated 6.5MB disk I/O.
- **Urban Cooling Intervention Simulator:** What-if policy lab evaluating hypothetical green canopy expansion, permeable ground conversion, and high-albedo cool roofs with physical cooling mechanism explanations.
- **Explainable AI (XAI) Transparency:** Dynamic permutation importance (MDA) on held-out test data alongside tree Gini impurity (MDI) and local feature drivers relative to regional medians.
- **Spatial Microclimate Explorer:** Interactive Leaflet GIS map with CartoDB Dark Matter, Positron Light, and OpenStreetMap tile layers with 6 Mumbai microclimate study archetypes.
- **Audit Report Generator:** One-click structured environmental assessment report export (JSON).
- **Automated Test Suite:** Built-in `pytest` test suite with 10 comprehensive test cases covering endpoints, boundary conditions, input validation, and simulation.

---

## Project Structure

```text
HeatLens_AI_Starter_Project/
├── app/
│   ├── main.py                  # FastAPI server, in-memory cache, uncertainty & inference
│   └── static/
│       ├── index.html           # Accessible, semantic dashboard UI
│       ├── styles.css           # Glassmorphism design system & dark/light theme
│       └── app.js               # Leaflet GIS, debounced inference, sliders, chart logic
├── data/
│   ├── demo_synthetic.csv       # Reproducible synthetic microclimate dataset (1,800 rows)
│   ├── demo_sample_rows.csv     # Sample observation rows
│   └── README.md                # Data documentation
├── docs/
│   ├── DATA_SOURCES.md          # Satellite integration roadmap (Landsat, Sentinel, NASA)
│   └── VIVA_GUIDE.md            # Comprehensive viva preparation handbook (25 Q&As)
├── models/
│   ├── model.joblib             # Serialized Random Forest bundle & feature statistics
│   ├── metrics.json             # Benchmark comparison & train/test evaluation metrics
│   └── feature_importance.json  # Permutation & Gini feature importance metrics
├── scripts/
│   └── train_model.py           # Reproducible training & evaluation pipeline (Fixed Seed 42)
├── tests/
│   └── test_api.py              # Automated pytest test suite (10 test cases)
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## Quickstart Guide

### Option A: Windows Command Prompt (CMD) — Recommended for Windows

Open Command Prompt (`cmd.exe`) in the project directory:

```bat
:: 1. Create Python virtual environment
py -m venv .venv

:: 2. Activate the virtual environment
.venv\Scripts\activate.bat

:: 3. Upgrade pip and install all dependencies
python -m pip install -r requirements.txt

:: 4. Train the Random Forest model and generate evaluation metrics
python scripts\train_model.py

:: 5. Run automated backend tests
pytest tests\test_api.py -v

:: 6. Launch the FastAPI development server
uvicorn app.main:app --reload
```

Then open your browser at **`http://127.0.0.1:8000`**.  
Interactive Swagger API documentation is available at **`http://127.0.0.1:8000/docs`**.

---

### Option B: Windows PowerShell

Open PowerShell in the project directory:

```powershell
# 1. Create Python virtual environment
py -m venv .venv

# 2. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Train model
python scripts/train_model.py

# 5. Run tests
pytest tests/test_api.py -v

# 6. Launch server
uvicorn app.main:app --reload
```

*(Note: If PowerShell displays an `Execution_Policies` script error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` or simply use Command Prompt).*

---

### Option C: macOS / Linux

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Train model
python scripts/train_model.py

# 4. Run tests
pytest tests/test_api.py -v

# 5. Launch server
uvicorn app.main:app --reload
```

---

## API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main environmental analytics dashboard |
| `GET` | `/api/health` | Health check, model status, and cache verification |
| `GET` | `/api/summary` | Complete training/test evaluation metrics & baseline comparisons |
| `GET` | `/api/health` | Service health, model status, and NASA POWER dataset availability |
| `GET` | `/api/summary` | Model candidate held-out test benchmarks (MAE, RMSE, R²) |
| `GET` | `/api/locations` | Microclimate study points (`scope=core` default for 6 sites, `scope=all` for full 23+ sites, `scope=metros`) |
| `GET` | `/api/places/search` | Search places by city, locality, category, or latitude,longitude coordinates |
| `GET` | `/api/places/{place_id}` | Detailed profile for an individual place or metropolitan benchmark |
| `GET` | `/api/feature-importance` | Permutation importance (MDA) and Gini impurity (MDI) metrics |
| `GET` | `/api/feature-stats` | Feature summary statistics (means, medians, IQRs) |
| `GET` | `/api/environmental-data` | Genuine observed NASA POWER daily meteorological records for Mumbai |
| `GET` | `/api/environmental-data/catalogue` | Authoritative remote-sensing product specifications (Landsat, Sentinel-2, ECOSTRESS, NASA POWER) |
| `GET` | `/api/environmental-data/download` | Direct file download of real environmental data (`format=csv` or `format=json`) |
| `POST` | `/api/predict` | Model inference with 95% tree-ensemble dispersion confidence intervals |
| `POST` | `/api/simulate` | Simulates hypothetical urban cooling scenarios and warming comparisons |
| `POST` | `/api/export-report` | Generates exportable structured assessment report (JSON) |
| `GET` | `/docs` | Interactive Swagger / OpenAPI documentation |

### Example Prediction Request (`POST /api/predict`)

```json
{
  "ndvi": 0.22,
  "impervious_pct": 78.0,
  "tree_canopy_pct": 10.0,
  "albedo": 0.16,
  "air_temp_c": 35.0,
  "relative_humidity_pct": 62.0
}
```

### Example Prediction Response

```json
{
  "score": 68.3,
  "uncertainty_std": 2.34,
  "tree_dispersion_interval": {
    "lower": 63.7,
    "upper": 72.9,
    "std": 2.34,
    "method": "empirical_tree_estimator_std",
    "multiplier": 1.96,
    "limitations": "Measures variance across 220 decorrelated decision trees on synthetic features; not calibrated physical uncertainty."
  },
  "risk_tier": "High Relative Risk",
  "badge_color": "#ef4444",
  "interpretation": "Elevated thermal risk driven by heavy impervious surfaces and reduced vegetative canopy shade.",
  "unit": "synthetic relative heat-risk index (0–100)",
  "data_status": "SYNTHETIC DEMO — NOT GROUND-CALIBRATED OBSERVATION"
}
```

---

## Machine Learning Architecture & Evaluation

- **Model:** `RandomForestRegressor` from `scikit-learn`
- **Ensemble Size:** 220 de-correlated decision trees
- **Regularization:** `min_samples_leaf=3`, fixed random state `seed=42`
- **Features (6):**
  1. `ndvi`: Normalized Difference Vegetation Index ($-0.2$ to $+1.0$)
  2. `impervious_pct`: Impervious surface coverage ($0$ to $100\%$)
  3. `tree_canopy_pct`: Tree crown coverage ($0$ to $100\%$)
  4. `albedo`: Surface solar reflectance ($0.05$ to $0.60$)
  5. `air_temp_c`: Ambient 2m air temperature ($-10$ to $60^\circ\text{C}$)
  6. `relative_humidity_pct`: Atmospheric moisture ($0$ to $100\%$)
- **Evaluation Splits:** $80\%$ Train ($1,440$ samples) / $20\%$ Test ($360$ samples)
- **Held-Out Test Metrics:**
  - Test MAE: **3.613** (vs. Dummy Mean 11.311)
  - Test RMSE: **4.775** (vs. Dummy Mean 13.278)
  - Test $R^2$: **0.871** (vs. Dummy Mean -0.001, Ridge Linear 0.861)
  - Train $R^2$: **0.960** (Overfitting delta: **0.089**)

---

## Automated Verification & Test Suite

The platform includes a comprehensive 22-test automated test suite in `tests/test_api.py`:

```bash
# Run complete test suite
.venv\Scripts\python.exe -m pytest tests/ -v
```

Tests cover:
- Endpoint health and status responses
- Observed environmental data and daily observation structures
- Location querying with backward-compatible `scope` parameters
- Free-text place search and coordinate parsing
- Single-place detailed retrieval with 404 validation
- Remote-sensing data catalogue metadata schema
- Direct CSV and JSON dataset downloads
- Prediction boundary clipping, extreme inputs, and Pydantic validation errors
- Tree-dispersion confidence interval formatting
- Scenario simulation arithmetic (cooling reductions, zero delta, and warming increases)
- Environmental assessment report generation and provenance tracking

---

## Academic Examination & Viva Preparation

For a complete guide to presenting this project during academic defense, including architectural explanations, mathematical derivations, and 25 anticipated viva questions with high-scoring answers, inspect [`docs/VIVA_GUIDE.md`](docs/VIVA_GUIDE.md).

---

## License & Attribution

This project is released under the MIT License for educational and research prototyping.
All satellite data integration guidelines cite official USGS Landsat, ESA Copernicus, and NASA POWER documentation.
