"""
HeatLens AI — Genuine Environmental Data Ingestion & Validation
NASA POWER Meteorology API Ingestion Workflow for Mumbai Study Area

Source: NASA POWER (Prediction of Worldwide Energy Resources)
Provider: NASA Langley Research Center / GMAO MERRA-2
Community: Renewable Energy (RE)
Study Area: Mumbai Metropolitan Region (Lat: 19.0760, Lon: 72.8777)
Licensing: NASA Open Data Policy (Public Domain, Free Academic Access)
"""

from pathlib import Path
import datetime
import json
import httpx
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

OUT_JSON = DATA_DIR / "mumbai_nasa_power_observed.json"
OUT_CSV = DATA_DIR / "mumbai_nasa_power_observed.csv"

# Configuration for Mumbai Metropolitan Area
LATITUDE = 19.0760
LONGITUDE = 72.8777
START_DATE = "20240501"  # May 1, 2024 (Summer Peak)
END_DATE = "20240531"    # May 31, 2024

PARAMETERS = [
    "T2M",               # Temperature at 2 Meters (°C)
    "T2M_MAX",           # Maximum Temperature at 2 Meters (°C)
    "T2M_MIN",           # Minimum Temperature at 2 Meters (°C)
    "RH2M",              # Relative Humidity at 2 Meters (%)
    "ALLSKY_SFC_SW_DWN", # All Sky Surface Shortwave Downward Irradiance (MJ/m^2/day)
    "WS2M"               # Wind Speed at 2 Meters (m/s)
]

VALIDATION_RANGES = {
    "T2M": (10.0, 50.0),               # °C
    "T2M_MAX": (15.0, 55.0),           # °C
    "T2M_MIN": (5.0, 40.0),            # °C
    "RH2M": (5.0, 100.0),              # %
    "ALLSKY_SFC_SW_DWN": (0.0, 35.0),  # MJ/m^2/day
    "WS2M": (0.0, 35.0)                # m/s
}

def fetch_nasa_power_records(lat: float, lon: float, start: str, end: str) -> dict:
    param_str = ",".join(PARAMETERS)
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters={param_str}&community=RE&longitude={lon}&latitude={lat}"
        f"&start={start}&end={end}&format=JSON"
    )
    print(f"[1/4] Querying NASA POWER API for Mumbai ({lat}°N, {lon}°E)...")
    print(f"      URL: {url}")
    
    with httpx.Client(timeout=25.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
        return resp.json()

def validate_and_process_records(raw_data: dict) -> tuple[pd.DataFrame, dict]:
    print("[2/4] Validating schema, numeric ranges, units, and missing-value flags...")
    
    properties = raw_data.get("properties", {})
    parameters = properties.get("parameter", {})
    
    for p in PARAMETERS:
        if p not in parameters:
            raise ValueError(f"Missing required meteorological parameter: {p}")
            
    dates = sorted(list(parameters["T2M"].keys()))
    if not dates:
        raise ValueError("Received zero daily records from NASA POWER API")
        
    records = []
    for d_str in dates:
        # Parse date YYYYMMDD
        dt = datetime.datetime.strptime(d_str, "%Y%m%d").date()
        rec = {
            "date": dt.isoformat(),
            "year": dt.year,
            "month": dt.month,
            "day": dt.day,
        }
        
        for p in PARAMETERS:
            val = parameters[p].get(d_str)
            if val is None or val == -999.0 or val == -999:
                raise ValueError(f"NASA POWER returned missing-data flag (-999.0) on {d_str} for {p}")
                
            # Range check
            min_valid, max_valid = VALIDATION_RANGES[p]
            if not (min_valid <= val <= max_valid):
                raise ValueError(
                    f"Parameter {p} value {val} out of physical bounds [{min_valid}, {max_valid}] on {d_str}"
                )
            rec[p] = round(float(val), 2)
            
        records.append(rec)
        
    df = pd.DataFrame(records)
    
    # Compute detailed summary statistics distinguishing monthly means from peak extremes
    peak_max_idx = df["T2M_MAX"].idxmax()
    lowest_min_idx = df["T2M_MIN"].idxmin()
    
    stats = {
        "observation_count": len(df),
        "date_range": {
            "start": df["date"].min(),
            "end": df["date"].max(),
        },
        "metrics": {
            # Core monthly means
            "monthly_mean_daily_avg_temp_c": round(float(df["T2M"].mean()), 2),
            "monthly_mean_daily_max_temp_c": round(float(df["T2M_MAX"].mean()), 2),
            "monthly_mean_daily_min_temp_c": round(float(df["T2M_MIN"].mean()), 2),
            "mean_humidity_pct": round(float(df["RH2M"].mean()), 1),
            "mean_solar_irradiance_mj_m2": round(float(df["ALLSKY_SFC_SW_DWN"].mean()), 2),
            "mean_wind_speed_ms": round(float(df["WS2M"].mean()), 2),
            # Single-day peak diurnal extremes with exact dates
            "peak_single_day_max_temp_c": round(float(df.loc[peak_max_idx, "T2M_MAX"]), 2),
            "peak_single_day_date": df.loc[peak_max_idx, "date"],
            "lowest_single_day_min_temp_c": round(float(df.loc[lowest_min_idx, "T2M_MIN"]), 2),
            "lowest_single_day_date": df.loc[lowest_min_idx, "date"],
            # Backwards compatibility keys
            "mean_temp_c": round(float(df["T2M"].mean()), 2),
            "max_temp_c": round(float(df.loc[peak_max_idx, "T2M_MAX"]), 2),
            "min_temp_c": round(float(df.loc[lowest_min_idx, "T2M_MIN"]), 2),
        }
    }
    
    return df, stats

def save_provenance_data(df: pd.DataFrame, summary_stats: dict, raw_json: dict):
    print("[3/4] Storing validated dataset with comprehensive provenance metadata...")
    
    # Save CSV
    df.to_csv(OUT_CSV, index=False)
    
    # Construct complete provenance envelope
    provenance_doc = {
        "dataset_name": "NASA POWER Mumbai Metropolitan Meteorological Observations",
        "provenance_status": "GRIDDED_METEOROLOGY_NASA_POWER_MERRA2",
        "data_license": "NASA Open Data Policy (Public Domain, Free Academic Use)",
        "provider": "NASA Langley Research Center Atmospheric Science Data Center",
        "source_system": "Global Modeling and Assimilation Office (GMAO) MERRA-2 & CERES/GEWEX Solar Assimilation",
        "data_nature": (
            "Gridded meteorological reanalysis and satellite model assimilation on a 0.5° × 0.625° grid (~50 km cell). "
            "These values represent regional ambient atmospheric boundary conditions and are NOT equivalent to "
            "in-situ neighborhood ground thermometers or satellite radiometric skin Land Surface Temperature (LST)."
        ),
        "official_documentation_url": "https://power.larc.nasa.gov/",
        "spatial_coverage": {
            "target_location": "Mumbai, Maharashtra, India",
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "grid_resolution": "0.5 x 0.625 degrees",
        },
        "temporal_coverage": {
            "start_date": summary_stats["date_range"]["start"],
            "end_date": summary_stats["date_range"]["end"],
            "days_recorded": summary_stats["observation_count"],
        },
        "ingestion_timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "summary_statistics": summary_stats["metrics"],
        "variable_definitions": {
            "T2M": {"name": "Daily Average 2m Air Temperature", "unit": "°C", "nature": "Synoptic Ambient Air Temperature"},
            "T2M_MAX": {"name": "Maximum Daily 2m Air Temperature", "unit": "°C", "nature": "Diurnal Maximum"},
            "T2M_MIN": {"name": "Minimum Daily 2m Air Temperature", "unit": "°C", "nature": "Diurnal Minimum"},
            "RH2M": {"name": "Relative Humidity at 2 Meters", "unit": "%", "nature": "Atmospheric Moisture"},
            "ALLSKY_SFC_SW_DWN": {"name": "All-Sky Surface Downward Shortwave Irradiance", "unit": "MJ/m^2/day", "nature": "Surface Solar Flux"},
            "WS2M": {"name": "Wind Speed at 2 Meters", "unit": "m/s", "nature": "Near-Surface Atmospheric Ventilation"}
        },
        "daily_observations": df.to_dict(orient="records"),
        "scientific_distinction": (
            "These meteorological parameters represent gridded assimilation estimates for regional atmospheric conditions from NASA POWER. "
            "They contrast fundamentally with HeatLens AI's microclimate risk score, which is a synthetic demonstration index (0–100)."
        )
    }
    
    OUT_JSON.write_text(json.dumps(provenance_doc, indent=2), encoding="utf-8")
    print(f"[4/4] Successfully saved:\n      - {OUT_JSON.name}\n      - {OUT_CSV.name}")

def main():
    print("=" * 70)
    print(" HeatLens AI — Real Environmental Data Ingestion Workflow")
    print(" Source: NASA POWER Public API (Mumbai Study Extent)")
    print("=" * 70)
    
    try:
        raw_data = fetch_nasa_power_records(LATITUDE, LONGITUDE, START_DATE, END_DATE)
        df, summary_stats = validate_and_process_records(raw_data)
        save_provenance_data(df, summary_stats, raw_data)
        
        print("\n" + "=" * 70)
        print(" INGESTION & VALIDATION COMPLETE — SUMMARY STATISTICS")
        print("=" * 70)
        print(f" Period: {summary_stats['date_range']['start']} to {summary_stats['date_range']['end']}")
        print(f" Total Daily Records: {summary_stats['observation_count']}")
        print(f" Mean 2m Air Temp:    {summary_stats['metrics']['mean_temp_c']} °C")
        print(f" Max Daily Air Temp:   {summary_stats['metrics']['max_temp_c']} °C")
        print(f" Min Daily Air Temp:   {summary_stats['metrics']['min_temp_c']} °C")
        print(f" Mean Relative Humid:  {summary_stats['metrics']['mean_humidity_pct']} %")
        print(f" Mean Solar Flux:      {summary_stats['metrics']['mean_solar_irradiance_mj_m2']} MJ/m²/day")
        print("=" * 70)
        return 0
    except Exception as e:
        print(f"[ERROR] Data ingestion failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
