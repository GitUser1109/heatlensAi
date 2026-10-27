"""
HeatLens AI — FastAPI Application & Microclimate Inference Engine
CSE (AIML) Environmental Studies Prototype

Features:
- In-memory cached model loading (zero disk I/O per request)
- Defensible prediction uncertainty via Random Forest tree-ensemble variance
- Comprehensive scenario simulator with pre-configured cooling interventions
- Explainable AI endpoints (feature importance and local feature contributions)
- Input validation with descriptive error guidance and sensible defaults
- Exportable environmental assessment reports (JSON and printable Markdown)
- Explicit synthetic data provenance disclaimers throughout all API responses
"""

from __future__ import annotations

from pathlib import Path
from contextlib import asynccontextmanager
import datetime
import json
from typing import Optional, List
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, status, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

from app.places import search_places, get_location_by_id, CORE_LOCATIONS, ALL_LOCATIONS
from app.data_catalogue import get_product_catalogue

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "model.joblib"
METRICS_PATH = ROOT / "models" / "metrics.json"
IMPORTANCE_PATH = ROOT / "models" / "feature_importance.json"
REAL_DATA_PATH = ROOT / "data" / "mumbai_nasa_power_observed.json"

FEATURES = [
    "ndvi",
    "impervious_pct",
    "tree_canopy_pct",
    "albedo",
    "air_temp_c",
    "relative_humidity_pct",
]

# Global in-memory cache for fast, non-blocking inference
CACHE = {
    "bundle": None,
    "metrics": None,
    "importance": None,
    "real_data": None,
}

def load_cached_bundle(force_reload: bool = False):
    """Load model artifact into memory once at startup to prevent repeated disk I/O."""
    if CACHE["bundle"] is not None and not force_reload:
        return CACHE["bundle"]
    if not MODEL_PATH.exists():
        return None
    try:
        CACHE["bundle"] = joblib.load(MODEL_PATH)
        return CACHE["bundle"]
    except Exception as e:
        print(f"Error loading model bundle: {e}")
        return None

def read_json_file(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return default

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Preload model, metadata, and observed data into memory on startup
    load_cached_bundle()
    CACHE["metrics"] = read_json_file(METRICS_PATH, {})
    CACHE["importance"] = read_json_file(IMPORTANCE_PATH, [])
    CACHE["real_data"] = read_json_file(REAL_DATA_PATH, None)
    print("[OK] HeatLens AI: In-memory model and environmental data cache initialized.")
    yield
    CACHE.clear()

app = FastAPI(
    title="HeatLens AI API",
    description=(
        "Urban Heat Intelligence decision-support API for CSE (AIML) Environmental Studies. "
        "Demonstrates Random Forest regression, tree-ensemble uncertainty, explainable AI, "
        "and cooling intervention simulation on clearly labelled synthetic demonstration data."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

# Enable CORS for local testing flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=ROOT / "app" / "static"), name="static")

@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


# Custom validation exception handler for beginner-friendly, clean error messages
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err["loc"] if loc != "body")
        msg = err.get("msg", "Invalid value")
        errors.append(f"{field}: {msg}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Input Validation Error",
            "detail": "; ".join(errors),
            "errors": errors,
            "hint": "Check acceptable ranges: NDVI [-0.2 to 1.0], Percentages [0 to 100], Albedo [0.0 to 1.0], Temp [-10 to 60°C]."
        }
    )

# -------------------------------------------------------------------------
# Pydantic Schemas
# -------------------------------------------------------------------------

class PredictionInput(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ndvi": 0.22,
                "impervious_pct": 78.0,
                "tree_canopy_pct": 10.0,
                "albedo": 0.16,
                "air_temp_c": 35.0,
                "relative_humidity_pct": 62.0
            }
        }
    )

    ndvi: float = Field(
        default=0.25,
        ge=-0.2,
        le=1.0,
        description="Normalized Difference Vegetation Index (-0.2 to 1.0). Higher values indicate healthy green vegetation."
    )
    impervious_pct: float = Field(
        default=70.0,
        ge=0.0,
        le=100.0,
        description="Percentage of land covered by asphalt, concrete, or buildings (0 to 100%)."
    )
    tree_canopy_pct: float = Field(
        default=15.0,
        ge=0.0,
        le=100.0,
        description="Percentage of ground area shaded by mature tree crowns (0 to 100%)."
    )
    albedo: float = Field(
        default=0.18,
        ge=0.0,
        le=1.0,
        description="Surface solar reflectance fraction (0.0 to 1.0). Higher values indicate reflective cool surfaces."
    )
    air_temp_c: float = Field(
        default=34.0,
        ge=-10.0,
        le=60.0,
        description="Regional ambient meteorological air temperature in °C (-10 to 60°C)."
    )
    relative_humidity_pct: float = Field(
        default=65.0,
        ge=0.0,
        le=100.0,
        description="Ambient relative humidity percentage (0 to 100%)."
    )

class SimulationInput(BaseModel):
    baseline: PredictionInput
    delta_tree_canopy_pct: float = Field(
        default=15.0,
        ge=-50.0,
        le=50.0,
        description="Change in tree canopy coverage percentage points (e.g. +15%)."
    )
    delta_impervious_pct: float = Field(
        default=-10.0,
        ge=-50.0,
        le=50.0,
        description="Change in impervious surface percentage points (e.g. -10%)."
    )
    delta_albedo: float = Field(
        default=0.05,
        ge=-0.5,
        le=0.5,
        description="Change in surface albedo reflectance (e.g. +0.08 for cool roofs)."
    )
    preset_name: str = Field(
        default="Custom Intervention",
        description="Name of the hypothetical urban greening / cooling scenario."
    )

class ExportReportInput(BaseModel):
    location_name: str = Field(default="Custom Study Point")
    notes: str = Field(default="Urban heat-risk assessment and mitigation evaluation.")
    inputs: PredictionInput
    simulation: Optional[SimulationInput] = None

# -------------------------------------------------------------------------
# Core Helper Functions
# -------------------------------------------------------------------------

def assess_risk_level(score: float):
    if score < 35.0:
        return {
            "tier": "Low Relative Risk",
            "badge_color": "#10b981",  # Emerald
            "summary": "Environmental features (elevated vegetation or high albedo) provide favorable microclimate moderation."
        }
    elif score < 65.0:
        return {
            "tier": "Moderate Relative Risk",
            "badge_color": "#f59e0b",  # Amber
            "summary": "Moderate urban heat potential. Typical urban residential / mixed-use profile with balanced features."
        }
    else:
        return {
            "tier": "High Relative Risk",
            "badge_color": "#ef4444",  # Crimson
            "summary": "Dense impervious coverage, sparse vegetation, and high thermal mass create pronounced heat-island susceptibility."
        }

def compute_ensemble_prediction(model, input_dict: dict, feature_stats: Optional[dict] = None):
    """
    Computes ensemble mean prediction and tree-ensemble prediction uncertainty
    (standard deviation across all 220 decision trees). Also computes local
    feature deviations against the regional training baseline.
    """
    row_values = np.array([[input_dict[f] for f in FEATURES]])
    
    # Predict across each independent tree estimator
    tree_preds = np.array([tree.predict(row_values)[0] for tree in model.estimators_])
    
    mean_val = float(np.mean(tree_preds))
    std_val = float(np.std(tree_preds))
    
    score = float(np.clip(mean_val, 0.0, 100.0))
    ci_lower = float(np.clip(score - 1.96 * std_val, 0.0, 100.0))
    ci_upper = float(np.clip(score + 1.96 * std_val, 0.0, 100.0))
    risk_info = assess_risk_level(score)

    # Calculate local feature drivers relative to dataset median
    feature_drivers = []
    if feature_stats:
        for f in FEATURES:
            val = input_dict[f]
            med = feature_stats.get(f, {}).get("median", val)
            std = feature_stats.get(f, {}).get("std", 1.0) or 1.0
            z_diff = (val - med) / std
            
            # Determine directional tendency
            if f in ["impervious_pct", "air_temp_c", "relative_humidity_pct"]:
                elevates = val > med
            else:
                # ndvi, canopy, albedo cool
                elevates = val < med

            feature_drivers.append({
                "feature": f,
                "current_value": val,
                "baseline_median": med,
                "z_score": round(float(z_diff), 2),
                "influence": "Elevates Risk" if elevates else "Mitigates Risk",
                "delta_from_median": round(val - med, 2)
            })

    return {
        "score": round(score, 1),
        "uncertainty_std": round(std_val, 2),
        "tree_dispersion_interval": {
            "lower": round(ci_lower, 1),
            "upper": round(ci_upper, 1),
            "dispersion_std": round(std_val, 2),
            "type": "illustrative tree-dispersion interval (+/-1.96 sigma_trees)",
            "limitations": "Measures variance across 220 independent decision trees; not an empirically calibrated conformal or Bayesian prediction interval."
        },
        "confidence_interval_95": {
            "lower": round(ci_lower, 1),
            "upper": round(ci_upper, 1),
            "description": "Illustrative tree-dispersion interval (+/-1.96 sigma_trees) reflecting ensemble disagreement"
        },
        "risk_tier": risk_info["tier"],
        "badge_color": risk_info["badge_color"],
        "summary": risk_info["summary"],
        "feature_drivers": feature_drivers,
    }

# -------------------------------------------------------------------------
# API Endpoints
# -------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
def serve_home():
    return FileResponse(ROOT / "app" / "static" / "index.html")

@app.get("/api/health", tags=["System"])
def health():
    bundle = load_cached_bundle()
    has_real_data = REAL_DATA_PATH.exists()
    return {
        "status": "ok",
        "app_version": "2.0.0",
        "model_ready": bundle is not None,
        "n_estimators": len(bundle["model"].estimators_) if bundle else 0,
        "data_status": "OBSERVED_NASA_DATA_AVAILABLE" if has_real_data else "SYNTHETIC_DEMO_NOT_OBSERVED",
        "real_data_available": has_real_data,
        "model_type": "SYNTHETIC_RELATIVE_RISK_INDEX",
        "server_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "disclaimer": "HeatLens AI integrates genuine observed NASA POWER meteorological observations with a synthetic demonstration microclimate risk model."
    }

@app.get("/api/environmental-data", tags=["Observed Geospatial Data"])
def get_environmental_data():
    """
    Returns genuine observed meteorological records for the Mumbai metropolitan study area
    ingested from the NASA POWER (GMAO MERRA-2) public API.
    Includes provenance metadata, physical variable definitions, and observation stats.
    """
    if CACHE.get("real_data"):
        return CACHE["real_data"]
    data = read_json_file(REAL_DATA_PATH, None)
    if data:
        CACHE["real_data"] = data
        return data
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Observed NASA POWER environmental dataset not found. Run 'python scripts/ingest_real_data.py' to fetch and validate real Mumbai records."
    )

@app.get("/api/summary", tags=["Metadata"])
def get_summary():
    bundle = load_cached_bundle()
    if bundle and "metrics" in bundle:
        return bundle["metrics"]
    metrics = read_json_file(METRICS_PATH, None)
    if metrics:
        return metrics
    return {
        "dataset": "Model not trained yet",
        "warning": "Run 'python scripts/train_model.py' to generate model and metrics."
    }

@app.get("/api/feature-importance", tags=["Explainability"])
def get_feature_importance():
    bundle = load_cached_bundle()
    if bundle and "importance" in bundle:
        return bundle["importance"]
    return read_json_file(IMPORTANCE_PATH, [])

@app.get("/api/feature-stats", tags=["Explainability"])
def get_feature_stats():
    bundle = load_cached_bundle()
    if bundle and "feature_stats" in bundle:
        return {
            "features": FEATURES,
            "metadata": bundle.get("feature_metadata", {}),
            "stats": bundle["feature_stats"]
        }
    return {"features": FEATURES, "stats": {}}

@app.get("/api/locations", tags=["Spatial Data"])
def get_locations(
    scope: str = Query("core", description="Filter scope: 'core' returns 6 primary demo sites, 'all' returns complete pan-India & MMR catalogue"),
    search: Optional[str] = Query(None, description="Search by location name, city, or zone type"),
    city: Optional[str] = Query(None, description="Filter by city name (e.g. Mumbai, Delhi, Bengaluru)"),
    category: Optional[str] = Query(None, description="Filter by zone category: commercial, residential, industrial, vegetated, coastal, suburban")
):
    """
    Returns urban microclimate study locations with dynamic model predictions.
    Default scope 'core' returns the 6 validated Mumbai primary profiles (preserving test compatibility).
    Passing scope='all', search, city, or category queries the full 23+ Indian city and MMR neighbourhood catalogue.
    """
    bundle = load_cached_bundle()
    model = bundle["model"] if bundle else None
    stats = bundle.get("feature_stats", {}) if bundle else {}

    if scope == "metros":
        locs = [dict(loc) for loc in ALL_LOCATIONS if loc.get("provenance_type") == "REGIONAL_METRO_BENCHMARK"]
    elif search or city or category or scope == "all":
        locs = search_places(query=search or "", city=city or "", category=category or "")
    else:
        # Default: 6 core primary profiles (guaranteeing exact backward compatibility)
        locs = [dict(loc) for loc in CORE_LOCATIONS]

    if model:
        for loc in locs:
            input_dict = {
                "ndvi": loc["ndvi"],
                "impervious_pct": loc["impervious_pct"],
                "tree_canopy_pct": loc["tree_canopy_pct"],
                "albedo": loc["albedo"],
                "air_temp_c": loc["air_temp_c"],
                "relative_humidity_pct": loc["relative_humidity_pct"]
            }
            pred = compute_ensemble_prediction(model, input_dict, stats)
            loc["score"] = pred["score"]
            loc["uncertainty_std"] = pred["uncertainty_std"]
            loc["ci_lower"] = pred["confidence_interval_95"]["lower"]
            loc["ci_upper"] = pred["confidence_interval_95"]["upper"]
            loc["tree_dispersion_interval"] = pred["tree_dispersion_interval"]
            loc["risk_tier"] = pred["risk_tier"]
            loc["badge_color"] = pred["badge_color"]
            loc["feature_drivers"] = pred["feature_drivers"]

    return locs

@app.get("/api/places/search", tags=["Spatial Data"])
def search_places_endpoint(
    q: str = Query("", description="Free-text query for city, neighbourhood, or lat,lon coordinate pair"),
    city: Optional[str] = Query(None, description="Optional city filter"),
    category: Optional[str] = Query(None, description="Optional category filter")
):
    """
    Search places across India and Mumbai Metropolitan Region.
    Supports city names, neighbourhood names, zone types, and latitude,longitude coordinate strings.
    """
    bundle = load_cached_bundle()
    model = bundle["model"] if bundle else None
    stats = bundle.get("feature_stats", {}) if bundle else {}

    results = search_places(query=q, city=city or "", category=category or "")
    if model:
        for loc in results:
            input_dict = {
                "ndvi": loc["ndvi"],
                "impervious_pct": loc["impervious_pct"],
                "tree_canopy_pct": loc["tree_canopy_pct"],
                "albedo": loc["albedo"],
                "air_temp_c": loc["air_temp_c"],
                "relative_humidity_pct": loc["relative_humidity_pct"]
            }
            pred = compute_ensemble_prediction(model, input_dict, stats)
            loc["score"] = pred["score"]
            loc["uncertainty_std"] = pred["uncertainty_std"]
            loc["ci_lower"] = pred["confidence_interval_95"]["lower"]
            loc["ci_upper"] = pred["confidence_interval_95"]["upper"]
            loc["risk_tier"] = pred["risk_tier"]
            loc["badge_color"] = pred["badge_color"]
            loc["feature_drivers"] = pred["feature_drivers"]

    return results

@app.get("/api/places/{place_id}", tags=["Spatial Data"])
def get_place_detail(place_id: int):
    """
    Fetch comprehensive microclimate profile and data provenance metadata for a specific place ID.
    """
    loc = get_location_by_id(place_id)
    if not loc:
        raise HTTPException(status_code=404, detail=f"Place ID {place_id} not found in catalogue.")

    bundle = load_cached_bundle()
    if bundle and "model" in bundle:
        input_dict = {f: loc[f] for f in FEATURES}
        pred = compute_ensemble_prediction(bundle["model"], input_dict, bundle.get("feature_stats", {}))
        loc["score"] = pred["score"]
        loc["uncertainty_std"] = pred["uncertainty_std"]
        loc["ci_lower"] = pred["confidence_interval_95"]["lower"]
        loc["ci_upper"] = pred["confidence_interval_95"]["upper"]
        loc["tree_dispersion_interval"] = pred["tree_dispersion_interval"]
        loc["risk_tier"] = pred["risk_tier"]
        loc["badge_color"] = pred["badge_color"]
        loc["feature_drivers"] = pred["feature_drivers"]

    return loc

@app.get("/api/environmental-data/catalogue", tags=["Observed Geospatial Data"])
def get_environmental_catalogue():
    """
    Returns the formal metadata catalogue for satellite and reanalysis products
    (NASA POWER, USGS Landsat 8/9 ST, ESA Sentinel-2, NASA ECOSTRESS, ESA WorldCover).
    """
    return get_product_catalogue()

@app.get("/api/environmental-data/download", tags=["Observed Geospatial Data"])
def download_environmental_data(
    format: str = Query("csv", description="Export format: 'csv' for daily records, 'json' for full dataset with metadata")
):
    """
    Directly download real observed Mumbai meteorological datasets (May 2024).
    """
    csv_file = ROOT / "data" / "mumbai_nasa_power_observed.csv"
    json_file = ROOT / "data" / "mumbai_nasa_power_observed.json"

    if format.lower() == "csv":
        if not csv_file.exists():
            raise HTTPException(status_code=404, detail="CSV dataset file not found on server.")
        return FileResponse(
            path=csv_file,
            media_type="text/csv",
            filename="mumbai_nasa_power_may2024_observed.csv"
        )
    elif format.lower() == "json":
        if not json_file.exists():
            raise HTTPException(status_code=404, detail="JSON dataset file not found on server.")
        return FileResponse(
            path=json_file,
            media_type="application/json",
            filename="mumbai_nasa_power_may2024_observed.json"
        )
    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported format requested. Please specify 'csv' or 'json'."
        )

@app.post("/api/predict", tags=["Inference"])
def predict(payload: PredictionInput):
    """
    Run Random Forest model inference on provided environmental parameters.
    Returns:
    - Point prediction (0-100 relative index)
    - Ensemble tree-prediction standard deviation (uncertainty)
    - 95% confidence interval
    - Qualitative risk tier categorization
    - Local feature drivers relative to regional medians
    - Clear scientific disclaimers
    """
    bundle = load_cached_bundle()
    if bundle is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model file 'models/model.joblib' not found. Please run 'python scripts/train_model.py' first."
        )

    model = bundle["model"]
    stats = bundle.get("feature_stats", {})
    input_dict = payload.model_dump()

    res = compute_ensemble_prediction(model, input_dict, stats)

    return {
        "score": res["score"],
        "uncertainty_std": res["uncertainty_std"],
        "tree_dispersion_interval": res["tree_dispersion_interval"],
        "confidence_interval_95": res["confidence_interval_95"],
        "risk_tier": res["risk_tier"],
        "badge_color": res["badge_color"],
        "summary": res["summary"],
        "local_feature_drivers": res["feature_drivers"],
        "unit": "synthetic relative heat-risk index (0-100)",
        "inputs": input_dict,
        "data_status": "SYNTHETIC DEMO - NOT GROUND-CALIBRATED OBSERVATION",
        "interpretation": (
            f"Predicted {res['risk_tier']} ({res['score']}/100 +/- {res['uncertainty_std']}). "
            "This value is a synthetic index for software and pipeline demonstration; "
            "it is not a measured temperature in deg C or a validated weather forecast."
        )
    }

@app.post("/api/simulate", tags=["Inference"])
def simulate_scenario(payload: SimulationInput):
    """
    Simulates hypothetical microclimate cooling interventions by modifying baseline features.
    Computes before vs after predictions, delta shift, risk tier transition,
    and biophysical cooling mechanism explanation.
    """
    bundle = load_cached_bundle()
    if bundle is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model missing. Run 'python scripts/train_model.py'."
        )

    model = bundle["model"]
    stats = bundle.get("feature_stats", {})
    base_dict = payload.baseline.model_dump()

    # Create modified scenario with boundary clipping
    scenario_dict = dict(base_dict)
    
    # 1. Tree canopy increase
    new_canopy = np.clip(base_dict["tree_canopy_pct"] + payload.delta_tree_canopy_pct, 0.0, 100.0)
    scenario_dict["tree_canopy_pct"] = round(float(new_canopy), 2)
    
    # 2. Impervious surface reduction
    new_impervious = np.clip(base_dict["impervious_pct"] + payload.delta_impervious_pct, 0.0, 100.0)
    scenario_dict["impervious_pct"] = round(float(new_impervious), 2)
    
    # 3. Albedo change (e.g. reflective roofs/cool pavements)
    new_albedo = np.clip(base_dict["albedo"] + payload.delta_albedo, 0.0, 1.0)
    scenario_dict["albedo"] = round(float(new_albedo), 3)

    # 4. Vegetation index (NDVI) coupling: when canopy increases and imperviousness decreases, NDVI rises realistically
    canopy_gain_ratio = payload.delta_tree_canopy_pct / 100.0
    impervious_loss_ratio = -payload.delta_impervious_pct / 100.0
    ndvi_boost = 0.25 * max(0.0, canopy_gain_ratio) + 0.15 * max(0.0, impervious_loss_ratio)
    new_ndvi = np.clip(base_dict["ndvi"] + ndvi_boost, -0.2, 1.0)
    scenario_dict["ndvi"] = round(float(new_ndvi), 3)

    # Run predictions for both states
    base_res = compute_ensemble_prediction(model, base_dict, stats)
    scen_res = compute_ensemble_prediction(model, scenario_dict, stats)

    # Audited intervention arithmetic
    reduction_points = round(base_res["score"] - scen_res["score"], 1)
    
    if base_res["score"] > 0:
        percent_reduction = round((base_res["score"] - scen_res["score"]) / base_res["score"] * 100, 1)
    else:
        percent_reduction = 0.0

    if reduction_points > 0:
        outcome_label = "Net Risk Reduction"
        direction = "Cooling / Risk Reduction"
    elif reduction_points < 0:
        outcome_label = "Net Risk Increase"
        direction = "Warming / Risk Increase"
    else:
        outcome_label = "No Net Change"
        direction = "Neutral / No Change"

    delta_score = round(scen_res["score"] - base_res["score"], 1)

    return {
        "preset_name": payload.preset_name,
        "baseline": {
            "inputs": base_dict,
            "score": base_res["score"],
            "uncertainty_std": base_res["uncertainty_std"],
            "tree_dispersion_interval": base_res["tree_dispersion_interval"],
            "confidence_interval": base_res["confidence_interval_95"],
            "risk_tier": base_res["risk_tier"],
            "badge_color": base_res["badge_color"],
        },
        "scenario": {
            "inputs": scenario_dict,
            "score": scen_res["score"],
            "uncertainty_std": scen_res["uncertainty_std"],
            "tree_dispersion_interval": scen_res["tree_dispersion_interval"],
            "confidence_interval": scen_res["confidence_interval_95"],
            "risk_tier": scen_res["risk_tier"],
            "badge_color": scen_res["badge_color"],
        },
        "delta": {
            "score_change": delta_score,
            "risk_reduction_points": reduction_points,
            "percentage_reduction": percent_reduction,
            "outcome_label": outcome_label,
            "direction": direction,
            "percent_change": round((delta_score / base_res["score"] * 100), 1) if base_res["score"] > 0 else 0.0,
            "tier_transition": f"{base_res['risk_tier']} -> {scen_res['risk_tier']}",
        },
        "mechanism_explanation": (
            f"Applying {payload.preset_name} (tree canopy {payload.delta_tree_canopy_pct:+}%, "
            f"impervious {payload.delta_impervious_pct:+}%, albedo {payload.delta_albedo:+.2f}) "
            f"shifted the synthetic risk score from {base_res['score']} to {scen_res['score']} "
            f"({outcome_label}: {abs(reduction_points)} points / {abs(percent_reduction)}%). "
            "Biophysical cooling occurs via enhanced evapotranspiration, shade interception, and high solar reflectance. "
            "Note: This is a hypothetical model what-if comparison on synthetic demonstration indices, not a physical CFD simulation or measured temperature in deg C."
        ),
        "data_status": "SYNTHETIC_WHAT_IF_SCENARIO_NOT_MEASURED"
    }

@app.post("/api/export-report", tags=["Reporting"])
def export_report(payload: ExportReportInput):
    """
    Generates a structured, printable environmental decision-support report
    with timestamps, feature contributions, scenario comparisons, and scientific disclaimers.
    """
    bundle = load_cached_bundle()
    if bundle is None:
        raise HTTPException(status_code=503, detail="Model missing.")

    model = bundle["model"]
    stats = bundle.get("feature_stats", {})
    input_dict = payload.inputs.model_dump()
    pred_res = compute_ensemble_prediction(model, input_dict, stats)

    now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    report = {
        "title": "HeatLens AI — Urban Microclimate Assessment Report",
        "generated_at": now_str,
        "study_point": payload.location_name,
        "analyst_notes": payload.notes,
        "model_architecture": "RandomForestRegressor (220 trees, scikit-learn)",
        "prediction_summary": {
            "heat_risk_score": f"{pred_res['score']}/100",
            "uncertainty_interval": f"[{pred_res['confidence_interval_95']['lower']} – {pred_res['confidence_interval_95']['upper']}]",
            "risk_classification": pred_res["risk_tier"],
        },
        "environmental_inputs": input_dict,
        "feature_drivers": pred_res["feature_drivers"],
        "data_integrity_notice": (
            "CRITICAL DISCLAIMER: This assessment is generated using HeatLens AI Student Prototype v2.0. "
            "All model parameters, training points, and risk indices are derived from synthetic demonstration data. "
            "Do NOT use these metrics for municipal civil works or policy enforcement without ground calibration "
            "against verified USGS Landsat / NASA ECOSTRESS radiometric satellite sensors."
        )
    }

    # Include NASA POWER regional meteorological baseline if cached/available
    env_data = CACHE.get("real_data") or read_json_file(REAL_DATA_PATH, None)
    if env_data:
        report["regional_meteorological_baseline"] = {
            "dataset_name": env_data.get("dataset_name"),
            "data_nature": "Gridded meteorological reanalysis & satellite solar assimilation (GMAO MERRA-2), not direct ground weather station measurements",
            "provider": env_data.get("provider"),
            "documentation_url": env_data.get("official_documentation_url", "https://power.larc.nasa.gov/"),
            "spatial_coverage": env_data.get("spatial_coverage"),
            "temporal_coverage": env_data.get("temporal_coverage"),
            "summary_statistics": env_data.get("summary_statistics"),
            "available_records_count": len(env_data.get("daily_observations", [])),
        }

    if payload.simulation:
        sim_res = simulate_scenario(payload.simulation)
        report["scenario_evaluation"] = {
            "intervention_name": sim_res["preset_name"],
            "baseline_score": sim_res["baseline"]["score"],
            "intervention_score": sim_res["scenario"]["score"],
            "score_reduction": sim_res["delta"]["score_change"],
            "tier_shift": sim_res["delta"]["tier_transition"],
            "mechanism": sim_res["mechanism_explanation"],
        }

    return report
