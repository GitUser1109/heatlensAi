from pathlib import Path
import sys
import pytest

# Ensure project root is in sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.main import app, load_cached_bundle

@pytest.fixture(scope="session")
def client():
    # Force load bundle
    load_cached_bundle(force_reload=True)
    with TestClient(app) as test_client:
        yield test_client

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model_ready"] is True
    assert data["data_status"] in ["SYNTHETIC_DEMO_NOT_OBSERVED", "OBSERVED_NASA_DATA_AVAILABLE"]
    assert data["n_estimators"] == 220

def test_environmental_data_endpoint(client):
    response = client.get("/api/environmental-data")
    assert response.status_code == 200
    data = response.json()
    assert "NASA_POWER" in data["provenance_status"]
    assert "summary_statistics" in data
    stats = data["summary_statistics"]
    assert stats["monthly_mean_daily_avg_temp_c"] == 32.16
    assert stats["monthly_mean_daily_max_temp_c"] == 39.23
    assert stats["peak_single_day_max_temp_c"] == 40.86
    assert stats["peak_single_day_date"] == "2024-05-05"
    assert "daily_observations" in data
    assert len(data["daily_observations"]) == 31
    assert data["spatial_coverage"]["target_location"] == "Mumbai, Maharashtra, India"
    assert "data_nature" in data
    assert "reanalysis" in data["data_nature"].lower()

def test_summary_endpoint(client):
    response = client.get("/api/summary")
    assert response.status_code == 200
    data = response.json()
    assert "test_metrics" in data
    assert "train_metrics" in data
    assert "baseline_comparison" in data
    assert data["test_metrics"]["r2"] > 0.8
    assert "dummy_mean" in data["baseline_comparison"]
    assert "ridge_regression" in data["baseline_comparison"]
    assert len(data["features"]) == 6

def test_feature_importance_endpoint(client):
    response = client.get("/api/feature-importance")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6
    for item in data:
        assert "feature" in item
        assert "importance_mean" in item
        assert "physical_mechanism" in item
        assert "gini_importance" in item

def test_feature_stats_endpoint(client):
    response = client.get("/api/feature-stats")
    assert response.status_code == 200
    data = response.json()
    assert "stats" in data
    assert "ndvi" in data["stats"]
    assert "impervious_pct" in data["stats"]
    assert "median" in data["stats"]["impervious_pct"]

def test_locations_endpoint(client):
    response = client.get("/api/locations")
    assert response.status_code == 200
    locations = response.json()
    assert len(locations) == 6
    for loc in locations:
        assert "name" in loc
        assert "lat" in loc
        assert "lon" in loc
        assert "score" in loc
        assert "uncertainty_std" in loc
        assert "risk_tier" in loc
        assert 0.0 <= loc["score"] <= 100.0

def test_predict_endpoint_valid(client):
    payload = {
        "ndvi": 0.22,
        "impervious_pct": 78.0,
        "tree_canopy_pct": 10.0,
        "albedo": 0.16,
        "air_temp_c": 35.0,
        "relative_humidity_pct": 62.0
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert 0.0 <= data["score"] <= 100.0
    assert "uncertainty_std" in data
    assert data["uncertainty_std"] > 0
    assert "confidence_interval_95" in data
    ci = data["confidence_interval_95"]
    assert ci["lower"] <= data["score"] <= ci["upper"]
    assert "risk_tier" in data
    assert "local_feature_drivers" in data
    assert len(data["local_feature_drivers"]) == 6

def test_predict_boundary_inputs(client):
    # Minimum and maximum valid edge values
    edge_payload = {
        "ndvi": -0.2,
        "impervious_pct": 0.0,
        "tree_canopy_pct": 0.0,
        "albedo": 0.0,
        "air_temp_c": -10.0,
        "relative_humidity_pct": 0.0
    }
    response = client.post("/api/predict", json=edge_payload)
    assert response.status_code == 200
    assert 0.0 <= response.json()["score"] <= 100.0

def test_predict_validation_errors(client):
    # Impervious percentage cannot exceed 100%
    invalid_payload = {
        "ndvi": 0.22,
        "impervious_pct": 145.0,  # Invalid
        "tree_canopy_pct": 10.0,
        "albedo": 0.16,
        "air_temp_c": 35.0,
        "relative_humidity_pct": 62.0
    }
    response = client.post("/api/predict", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert "impervious_pct" in data["detail"]

def test_simulate_scenario(client):
    payload = {
        "baseline": {
            "ndvi": 0.15,
            "impervious_pct": 85.0,
            "tree_canopy_pct": 8.0,
            "albedo": 0.15,
            "air_temp_c": 36.0,
            "relative_humidity_pct": 60.0
        },
        "delta_tree_canopy_pct": 20.0,
        "delta_impervious_pct": -15.0,
        "delta_albedo": 0.10,
        "preset_name": "Urban Canopy & Cool Roof Expansion"
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["preset_name"] == "Urban Canopy & Cool Roof Expansion"
    assert "baseline" in data
    assert "scenario" in data
    assert "delta" in data
    delta = data["delta"]
    # Cooling should result in negative score_change and positive risk_reduction_points
    assert delta["score_change"] < 0
    assert delta["risk_reduction_points"] > 0
    assert delta["risk_reduction_points"] == round(data["baseline"]["score"] - data["scenario"]["score"], 1)
    assert delta["percentage_reduction"] > 0
    assert delta["outcome_label"] == "Net Risk Reduction"
    assert "mechanism_explanation" in data

def test_simulate_scenario_warming_increase(client):
    # Simulate a deforestation / paving scenario that increases thermal risk
    warming_payload = {
        "baseline": {
            "ndvi": 0.60,
            "impervious_pct": 20.0,
            "tree_canopy_pct": 55.0,
            "albedo": 0.25,
            "air_temp_c": 30.0,
            "relative_humidity_pct": 70.0
        },
        "delta_tree_canopy_pct": -30.0,
        "delta_impervious_pct": 40.0,
        "delta_albedo": -0.10,
        "preset_name": "Hypothetical Canopy Removal"
    }
    response = client.post("/api/simulate", json=warming_payload)
    assert response.status_code == 200
    data = response.json()
    delta = data["delta"]
    # Risk should increase
    assert delta["score_change"] > 0
    assert delta["risk_reduction_points"] < 0
    assert delta["outcome_label"] == "Net Risk Increase"
    assert delta["direction"] == "Warming / Risk Increase"

def test_predict_tree_dispersion_interval_and_limitations(client):
    payload = {
        "ndvi": 0.25,
        "impervious_pct": 70.0,
        "tree_canopy_pct": 15.0,
        "albedo": 0.18,
        "air_temp_c": 34.0,
        "relative_humidity_pct": 65.0
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "tree_dispersion_interval" in data
    tree_ci = data["tree_dispersion_interval"]
    assert "lower" in tree_ci
    assert "upper" in tree_ci
    assert "limitations" in tree_ci
    assert "decision trees" in tree_ci["limitations"]
    assert tree_ci["lower"] <= data["score"] <= tree_ci["upper"]

def test_export_report_endpoint(client):
    payload = {
        "location_name": "BKC Urban Hotspot",
        "notes": "Testing high impervious area intervention potential.",
        "inputs": {
            "ndvi": 0.12,
            "impervious_pct": 88.0,
            "tree_canopy_pct": 6.0,
            "albedo": 0.15,
            "air_temp_c": 35.5,
            "relative_humidity_pct": 64.0
        },
        "simulation": {
            "baseline": {
                "ndvi": 0.12,
                "impervious_pct": 88.0,
                "tree_canopy_pct": 6.0,
                "albedo": 0.15,
                "air_temp_c": 35.5,
                "relative_humidity_pct": 64.0
            },
            "delta_tree_canopy_pct": 25.0,
            "delta_impervious_pct": -20.0,
            "delta_albedo": 0.12,
            "preset_name": "District-Wide High Albedo & Tree Greening"
        }
    }
    response = client.post("/api/export-report", json=payload)
    assert response.status_code == 200
    report = response.json()
    assert "title" in report
    assert "study_point" in report
    assert "prediction_summary" in report
    assert "scenario_evaluation" in report
    assert "data_integrity_notice" in report
    assert "regional_meteorological_baseline" in report
    baseline = report["regional_meteorological_baseline"]
    assert "NASA POWER" in baseline["dataset_name"]
    assert baseline["available_records_count"] == 31
    assert "summary_statistics" in baseline

def test_simulate_scenario_zero_delta(client):
    payload = {
        "baseline": {
            "ndvi": 0.35,
            "impervious_pct": 50.0,
            "tree_canopy_pct": 25.0,
            "albedo": 0.20,
            "air_temp_c": 32.0,
            "relative_humidity_pct": 65.0
        },
        "delta_tree_canopy_pct": 0.0,
        "delta_impervious_pct": 0.0,
        "delta_albedo": 0.0,
        "preset_name": "Zero Change Scenario"
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    delta = data["delta"]
    assert delta["risk_reduction_points"] == 0.0
    assert delta["outcome_label"] == "No Net Change"
    assert delta["direction"] == "Neutral / No Change"

def test_simulate_boundary_clipping(client):
    payload = {
        "baseline": {
            "ndvi": 0.85,
            "impervious_pct": 90.0,
            "tree_canopy_pct": 80.0,
            "albedo": 0.40,
            "air_temp_c": 38.0,
            "relative_humidity_pct": 80.0
        },
        "delta_tree_canopy_pct": 50.0,   # 80 + 50 = 130 -> should clip to 100.0
        "delta_impervious_pct": -50.0,  # 90 - 50 = 40.0
        "delta_albedo": 0.5,            # 0.4 + 0.5 = 0.9 -> should clip to <= 1.0
        "preset_name": "Extreme Greening"
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    scen_inputs = data["scenario"]["inputs"]
    assert scen_inputs["tree_canopy_pct"] <= 100.0
    assert scen_inputs["albedo"] <= 1.0
    assert scen_inputs["ndvi"] <= 1.0

def test_export_report_without_simulation(client):
    payload = {
        "location_name": "Marine Drive Coastal Point",
        "notes": "Baseline assessment without intervention.",
        "inputs": {
            "ndvi": 0.20,
            "impervious_pct": 75.0,
            "tree_canopy_pct": 12.0,
            "albedo": 0.18,
            "air_temp_c": 33.5,
            "relative_humidity_pct": 72.0
        }
    }
    response = client.post("/api/export-report", json=payload)
    assert response.status_code == 200
    report = response.json()
    assert report["study_point"] == "Marine Drive Coastal Point"
    assert "scenario_evaluation" not in report
    assert "prediction_summary" in report


def test_scene6_scientific_audit_and_provenance(client):
    """
    Focused verification of Scene 6 data integrity:
    1. Distinguishes monthly mean daily max (39.23 °C) from peak extreme (40.86 °C on May 5, 2024).
    2. Identifies NASA POWER as GMAO MERRA-2 gridded reanalysis, not neighborhood ground sensors.
    3. Confirms model report separates synthetic demonstration from environmental baseline.
    """
    res = client.get("/api/environmental-data")
    assert res.status_code == 200
    data = res.json()

    # Verify provenance and nature
    assert "reanalysis" in data["data_nature"].lower()
    assert "MERRA-2" in data["provenance_status"] or "NASA_POWER" in data["provenance_status"]
    assert data["spatial_coverage"]["latitude"] == 19.076
    assert data["spatial_coverage"]["longitude"] == 72.8777
    assert data["temporal_coverage"]["days_recorded"] == 31
    assert data["temporal_coverage"]["start_date"] == "2024-05-01"
    assert data["temporal_coverage"]["end_date"] == "2024-05-31"

    # Verify exact calculated metrics
    stats = data["summary_statistics"]
    assert stats["monthly_mean_daily_avg_temp_c"] == 32.16
    assert stats["monthly_mean_daily_max_temp_c"] == 39.23
    assert stats["peak_single_day_max_temp_c"] == 40.86
    assert stats["peak_single_day_date"] == "2024-05-05"
    assert stats["lowest_single_day_min_temp_c"] == 23.84
    assert stats["lowest_single_day_date"] == "2024-05-03"
    assert stats["mean_humidity_pct"] == 59.9
    assert stats["mean_solar_irradiance_mj_m2"] == 6.83
    assert stats["mean_wind_speed_ms"] == 2.53

    # Check report export includes provenance and separation
    report_res = client.post("/api/export-report", json={
        "location_name": "Audit Test",
        "inputs": {"ndvi": 0.2, "impervious_pct": 50.0, "tree_canopy_pct": 20.0, "albedo": 0.2, "air_temp_c": 32.0, "relative_humidity_pct": 60.0}
    })
    assert report_res.status_code == 200
    report = report_res.json()
    assert "regional_meteorological_baseline" in report
    base = report["regional_meteorological_baseline"]
    assert base["available_records_count"] == 31
    assert "power.larc.nasa.gov" in base["documentation_url"]
    assert "data_integrity_notice" in report
    assert "synthetic" in report["data_integrity_notice"].lower()


def test_places_search_and_discovery(client):
    """Test City Explorer place search across text, city filters, and coordinates."""
    # 1. Text search for a Mumbai neighbourhood
    res = client.get("/api/places/search?q=Bandra")
    assert res.status_code == 200
    places = res.json()
    assert len(places) >= 1
    assert any("Bandra" in p["name"] for p in places)
    assert places[0]["city"] == "Mumbai"
    assert "score" in places[0]
    assert 0 <= places[0]["score"] <= 100

    # 2. Search for other Indian cities (Delhi, Bengaluru)
    res_delhi = client.get("/api/places/search?q=Delhi")
    assert res_delhi.status_code == 200
    delhi_places = res_delhi.json()
    assert len(delhi_places) >= 1
    assert any("Delhi" in p["city"] for p in delhi_places)
    assert delhi_places[0]["model_applicability"] == "REGIONAL_REFERENCE_ONLY"

    # 3. Coordinate parsing
    res_coord = client.get("/api/places/search?q=19.0760, 72.8777")
    assert res_coord.status_code == 200
    coord_results = res_coord.json()
    assert len(coord_results) == 1
    assert "Coordinate Point" in coord_results[0]["name"]
    assert coord_results[0]["lat"] == 19.076
    assert coord_results[0]["lon"] == 72.8777

    # 4. Category filter
    res_ind = client.get("/api/places/search?category=industrial")
    assert res_ind.status_code == 200
    ind_places = res_ind.json()
    assert len(ind_places) >= 1
    for p in ind_places:
        assert p["category"] == "industrial"


def test_place_detail_endpoint(client):
    """Test fetching single place by ID."""
    res = client.get("/api/places/1")
    assert res.status_code == 200
    place = res.json()
    assert place["id"] == 1
    assert "BKC" in place["name"] or "Bandra Kurla" in place["name"]
    assert "score" in place
    assert "uncertainty_std" in place

    # Non-existent ID returns 404
    res_404 = client.get("/api/places/999999")
    assert res_404.status_code == 404


def test_locations_with_scope_parameter(client):
    """Verify scope='core' preserves 6 locations while scope='all' returns full catalogue."""
    # Default (core) returns 6
    res_core = client.get("/api/locations")
    assert res_core.status_code == 200
    assert len(res_core.json()) == 6

    # Explicit scope=all returns 20+ locations
    res_all = client.get("/api/locations?scope=all")
    assert res_all.status_code == 200
    assert len(res_all.json()) >= 20


def test_environmental_catalogue_endpoint(client):
    """Verify formal metadata catalogue of satellite and reanalysis products."""
    res = client.get("/api/environmental-data/catalogue")
    assert res.status_code == 200
    catalogue = res.json()
    assert len(catalogue) >= 4
    product_ids = [p["product_id"] for p in catalogue]
    assert "nasa_power_meteorology" in product_ids
    assert "usgs_landsat_st" in product_ids
    assert "esa_sentinel2_msi" in product_ids
    assert "nasa_ecostress" in product_ids


def test_environmental_download_csv_and_json(client):
    """Verify real data export downloads in CSV and JSON formats."""
    # CSV download
    res_csv = client.get("/api/environmental-data/download?format=csv")
    assert res_csv.status_code == 200
    assert "text/csv" in res_csv.headers.get("content-type", "")
    assert "attachment" in res_csv.headers.get("content-disposition", "")
    assert b"T2M" in res_csv.content
    assert b"2024-05-01" in res_csv.content

    # JSON download
    res_json = client.get("/api/environmental-data/download?format=json")
    assert res_json.status_code == 200
    assert "application/json" in res_json.headers.get("content-type", "")
    json_data = res_json.json()
    assert "summary_statistics" in json_data
    assert len(json_data["daily_observations"]) == 31

    # Invalid format returns 400
    res_bad = client.get("/api/environmental-data/download?format=xml")
    assert res_bad.status_code == 400


