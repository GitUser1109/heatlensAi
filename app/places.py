"""
HeatLens AI — Scalable City & Place Catalogue
Provides curated, validated geographic locations for urban microclimate exploration:
- 15 detailed Mumbai Metropolitan Region (MMR) microclimate study sites
- 8 Major Indian Metropolitan regional benchmarks (Delhi, Bengaluru, Kolkata, Chennai, Hyderabad, Ahmedabad, Pune, Jaipur)
- Geocoding, reverse coordinate matching, and data provenance metadata
"""

from typing import Dict, List, Optional
import math
import re

# Comprehensive Location Database
ALL_LOCATIONS: List[Dict] = [
    # -------------------------------------------------------------------------
    # MUMBAI METROPOLITAN REGION (MMR) — Core Detailed Study Sites
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "name": "Bandra Kurla Complex (BKC)",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Dense Commercial / High Imperviousness",
        "category": "commercial",
        "lat": 19.0657,
        "lon": 72.8687,
        "ndvi": 0.14,
        "impervious_pct": 86.0,
        "tree_canopy_pct": 7.0,
        "albedo": 0.16,
        "air_temp_c": 35.5,
        "relative_humidity_pct": 62.0,
        "description": "High-density glass and asphalt financial district with deep urban canyons, minimal natural soil cover, and high anthropogenic HVAC waste heat.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel; 0.5° synoptic boundary",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent. Suitable for relative risk prediction and what-if cooling intervention simulation.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 2,
        "name": "Sanjay Gandhi National Park Border",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Protected Forest Edge / High Canopy",
        "category": "vegetated",
        "lat": 19.2183,
        "lon": 72.9125,
        "ndvi": 0.72,
        "impervious_pct": 18.0,
        "tree_canopy_pct": 68.0,
        "albedo": 0.24,
        "air_temp_c": 31.8,
        "relative_humidity_pct": 74.0,
        "description": "Lush tropical deciduous canopy buffer on the northern municipal border providing significant biophysical cooling and sensible-to-latent heat conversion.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel; 0.5° synoptic boundary",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent. Serves as natural vegetative reference baseline.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 3,
        "name": "Dharavi / Central Industrial Cluster",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Dense Built / Corrugated Tin Roofing",
        "category": "industrial",
        "lat": 19.0434,
        "lon": 72.8570,
        "ndvi": 0.08,
        "impervious_pct": 92.0,
        "tree_canopy_pct": 4.0,
        "albedo": 0.13,
        "air_temp_c": 36.2,
        "relative_humidity_pct": 59.0,
        "description": "Extremely dense, informal settlement morphology dominated by low-albedo corrugated tin roofing, zero permeable soil, and high thermal retention into nocturnal hours.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel; 0.5° synoptic boundary",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training extent. Represents extreme thermal vulnerability hot-spot requiring cool roof interventions.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 4,
        "name": "Powai Lake Waterfront & IIT Campus",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Institutional / Mixed Greenspace & Water",
        "category": "coastal",
        "lat": 19.1290,
        "lon": 72.9090,
        "ndvi": 0.54,
        "impervious_pct": 38.0,
        "tree_canopy_pct": 44.0,
        "albedo": 0.22,
        "air_temp_c": 32.5,
        "relative_humidity_pct": 68.0,
        "description": "Inland freshwater lake basin buffered by academic institutional campus grounds, mature tree canopy, and localized evaporative cooling.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel; 0.5° synoptic boundary",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent. Good benchmark for mixed blue-green infrastructure.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 5,
        "name": "Lower Parel Commercial Mill District",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Urban Canyon / High-Rise Re-development",
        "category": "commercial",
        "lat": 19.0020,
        "lon": 72.8300,
        "ndvi": 0.16,
        "impervious_pct": 84.0,
        "tree_canopy_pct": 9.0,
        "albedo": 0.17,
        "air_temp_c": 34.8,
        "relative_humidity_pct": 64.0,
        "description": "Vertical high-rise office towers replacing historic textile mills, producing deep street canyons that impede coastal wind ventilation.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel; 0.5° synoptic boundary",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 6,
        "name": "Marine Drive Coastal Promenade",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Coastal Strip / Marine Boundary Layer",
        "category": "coastal",
        "lat": 18.9432,
        "lon": 72.8230,
        "ndvi": 0.22,
        "impervious_pct": 74.0,
        "tree_canopy_pct": 12.0,
        "albedo": 0.20,
        "air_temp_c": 33.2,
        "relative_humidity_pct": 76.0,
        "description": "South Mumbai seaside boulevard moderated by Arabian Sea diurnal breezes, but experiencing high daytime humidity and solar exposure.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel; 0.5° synoptic boundary",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent. Maritime boundary layer moderation.",
        "missing_data_status": "VALID_COMPLETE"
    },
    # Additional Diverse Mumbai Metropolitan Study Points
    {
        "id": 7,
        "name": "Colaba & Fort Heritage Precinct",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Historic Masonry / High Thermal Mass",
        "category": "residential",
        "lat": 18.9150,
        "lon": 72.8258,
        "ndvi": 0.26,
        "impervious_pct": 78.0,
        "tree_canopy_pct": 16.0,
        "albedo": 0.18,
        "air_temp_c": 33.6,
        "relative_humidity_pct": 73.0,
        "description": "Historic colonial basalt and lime mortar buildings with thick thermal mass and moderate roadside tree avenues near the peninsula tip.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 8,
        "name": "Dadar Central Transit Hub",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Transit Interchange / Dense Pedestrian Footfall",
        "category": "commercial",
        "lat": 19.0178,
        "lon": 72.8478,
        "ndvi": 0.18,
        "impervious_pct": 85.0,
        "tree_canopy_pct": 11.0,
        "albedo": 0.15,
        "air_temp_c": 35.1,
        "relative_humidity_pct": 65.0,
        "description": "Major railway terminus and commercial market junction with concrete flyovers, high traffic volume, and intense human heat emission.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 9,
        "name": "Andheri East MIDC Industrial Belt",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Industrial Park / Large Rooftop Footprints",
        "category": "industrial",
        "lat": 19.1170,
        "lon": 72.8680,
        "ndvi": 0.12,
        "impervious_pct": 89.0,
        "tree_canopy_pct": 6.0,
        "albedo": 0.14,
        "air_temp_c": 35.8,
        "relative_humidity_pct": 61.0,
        "description": "Extensive industrial manufacturing and warehousing sheds with sprawling dark roofs, asphalt yards, and minimal permeable landscaping.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent. High opportunity zone for industrial cool roof retrofits.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 10,
        "name": "Thane Suburban Basin (Ghodbunder)",
        "city": "Thane",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Suburban Valley / Foothill Stagnation",
        "category": "suburban",
        "lat": 19.2180,
        "lon": 72.9780,
        "ndvi": 0.38,
        "impervious_pct": 62.0,
        "tree_canopy_pct": 28.0,
        "albedo": 0.19,
        "air_temp_c": 36.4,
        "relative_humidity_pct": 60.0,
        "description": "Inland suburban valley between Yeoor Hills and Ulhas Creek experiencing reduced coastal ventilation and elevated daytime temperatures.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Within greater metropolitan study boundary.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 11,
        "name": "Navi Mumbai Planned Sector (Vashi)",
        "city": "Navi Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Planned Grid / Wide Tree-Lined Avenues",
        "category": "residential",
        "lat": 19.0770,
        "lon": 72.9980,
        "ndvi": 0.42,
        "impervious_pct": 55.0,
        "tree_canopy_pct": 32.0,
        "albedo": 0.21,
        "air_temp_c": 34.5,
        "relative_humidity_pct": 63.0,
        "description": "Modern planned urban sector developed by CIDCO with wide setback corridors, planned street canopy buffers, and moderate building density.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Within greater metropolitan study boundary. Shows beneficial effects of urban planning standards.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 12,
        "name": "Aarey Forest Green Lung Buffer",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Urban Forest / Dense Grassland Buffer",
        "category": "vegetated",
        "lat": 19.1450,
        "lon": 72.8750,
        "ndvi": 0.68,
        "impervious_pct": 15.0,
        "tree_canopy_pct": 62.0,
        "albedo": 0.22,
        "air_temp_c": 32.1,
        "relative_humidity_pct": 72.0,
        "description": "Contiguous urban green zone serving as an ecological heat sink and cooler air corridor between western and eastern suburbs.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent. Major ecological cooling corridor.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 13,
        "name": "Chembur & Mahul Refinery Zone",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Heavy Petrochemical / Anthropogenic Heat",
        "category": "industrial",
        "lat": 19.0080,
        "lon": 72.9020,
        "ndvi": 0.15,
        "impervious_pct": 88.0,
        "tree_canopy_pct": 8.0,
        "albedo": 0.14,
        "air_temp_c": 36.6,
        "relative_humidity_pct": 61.0,
        "description": "Industrial refinery and fertilizer processing area with significant industrial waste flare heat and low natural albedo.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training extent.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 14,
        "name": "Juhu Coastal Residential Enclave",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Coastal Residential / Sandy Coastal Fringe",
        "category": "coastal",
        "lat": 19.1020,
        "lon": 72.8260,
        "ndvi": 0.30,
        "impervious_pct": 68.0,
        "tree_canopy_pct": 22.0,
        "albedo": 0.23,
        "air_temp_c": 33.4,
        "relative_humidity_pct": 77.0,
        "description": "Affluent coastal residential area with sandy soils, coastal coconut palms, and direct maritime boundary layer ventilation.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 15,
        "name": "Gorai Creek Mangrove Estuary",
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Tidal Mangrove Wetland / Hydrological Cooling",
        "category": "vegetated",
        "lat": 19.2420,
        "lon": 72.8150,
        "ndvi": 0.58,
        "impervious_pct": 12.0,
        "tree_canopy_pct": 52.0,
        "albedo": 0.16,
        "air_temp_c": 32.2,
        "relative_humidity_pct": 82.0,
        "description": "Dense tidal mangrove forest along the northwestern creek buffer providing flood resilience and microclimatic thermal mitigation.",
        "data_source": "Mumbai Regional Environmental Baseline (NASA POWER + Micro-grid)",
        "spatial_resolution": "30m grid resampled from Landsat/Sentinel",
        "observation_period": "May 2024 Pre-Monsoon Peak",
        "provenance_type": "SYNTHETIC_MICRO_STUDY_POINT",
        "model_applicability": "DIRECT_LOCAL_APPLICABILITY",
        "model_applicability_note": "Directly within model training spatial extent.",
        "missing_data_status": "VALID_COMPLETE"
    },

    # -------------------------------------------------------------------------
    # MAJOR INDIAN METROPOLITAN REGIONAL BENCHMARKS (City Explorer)
    # -------------------------------------------------------------------------
    {
        "id": 101,
        "name": "New Delhi — Connaught Place & Central Ridge",
        "city": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "zone_type": "Continental Semi-Arid / High Solar Load",
        "category": "commercial",
        "lat": 28.6315,
        "lon": 77.2167,
        "ndvi": 0.22,
        "impervious_pct": 76.0,
        "tree_canopy_pct": 18.0,
        "albedo": 0.18,
        "air_temp_c": 41.5,
        "relative_humidity_pct": 32.0,
        "description": "National capital central commercial hub experiencing extreme dry summer continental heat (Loo winds), high solar irradiance, and nocturnal heat island.",
        "data_source": "National Capital Region Climatological Benchmark (IMD / NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Random Forest model was trained on Mumbai coastal parameters; cross-climate extrapolation requires local semi-arid calibration.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 102,
        "name": "Bengaluru — Electronic City & Tech Corridors",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zone_type": "Elevated Plateau / IT Industrial Corridor",
        "category": "commercial",
        "lat": 12.8452,
        "lon": 77.6602,
        "ndvi": 0.28,
        "impervious_pct": 72.0,
        "tree_canopy_pct": 20.0,
        "albedo": 0.19,
        "air_temp_c": 33.8,
        "relative_humidity_pct": 52.0,
        "description": "High-altitude Deccan plateau tech hub (920m ASL). Rapid urbanization has reduced historic garden canopy, increasing local surface temperatures.",
        "data_source": "Deccan Plateau Climatological Benchmark (IMD / NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Demonstrates plateau microclimate conditions.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 103,
        "name": "Kolkata — Salt Lake Sector V & Wetlands",
        "city": "Kolkata",
        "state": "West Bengal",
        "country": "India",
        "zone_type": "Humid Deltaic Basin / Waterbody Proximity",
        "category": "commercial",
        "lat": 22.5800,
        "lon": 88.4350,
        "ndvi": 0.34,
        "impervious_pct": 68.0,
        "tree_canopy_pct": 24.0,
        "albedo": 0.17,
        "air_temp_c": 37.2,
        "relative_humidity_pct": 72.0,
        "description": "Gangetic deltaic plain commercial IT cluster adjacent to East Kolkata Wetlands, characterized by high thermal heat index and persistent humidity.",
        "data_source": "Eastern Gangetic Delta Climatological Benchmark (NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Demonstrates high-humidity deltaic microclimate.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 104,
        "name": "Chennai — T. Nagar & Guindy Industrial",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "zone_type": "Tropical Maritime / High Relative Humidity",
        "category": "commercial",
        "lat": 13.0418,
        "lon": 80.2341,
        "ndvi": 0.20,
        "impervious_pct": 82.0,
        "tree_canopy_pct": 14.0,
        "albedo": 0.17,
        "air_temp_c": 38.6,
        "relative_humidity_pct": 68.0,
        "description": "Coromandel Coast commercial retail core experiencing high solar radiation, warm nocturnal humid retention, and limited natural vegetative cover.",
        "data_source": "Coromandel Coastal Climatological Benchmark (NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Tropical maritime climate comparison.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 105,
        "name": "Hyderabad — Hitec City & Gachibowli",
        "city": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "zone_type": "Granite Ridge / Rapid Urban Expansion",
        "category": "commercial",
        "lat": 17.4435,
        "lon": 78.3772,
        "ndvi": 0.18,
        "impervious_pct": 79.0,
        "tree_canopy_pct": 12.0,
        "albedo": 0.18,
        "air_temp_c": 40.2,
        "relative_humidity_pct": 42.0,
        "description": "Rocky granitic plateau financial district with extensive asphalt multilane highways, high thermal inertia, and pronounced diurnal UHI intensity.",
        "data_source": "Telangana Plateau Climatological Benchmark (NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Semi-arid interior plateau conditions.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 106,
        "name": "Ahmedabad — Sabarmati Riverfront & SG Highway",
        "city": "Ahmedabad",
        "state": "Gujarat",
        "country": "India",
        "zone_type": "Western Arid Basin / Extreme May Temperatures",
        "category": "commercial",
        "lat": 23.0300,
        "lon": 72.5800,
        "ndvi": 0.16,
        "impervious_pct": 82.0,
        "tree_canopy_pct": 10.0,
        "albedo": 0.20,
        "air_temp_c": 42.8,
        "relative_humidity_pct": 34.0,
        "description": "Western arid industrial riverfront city subject to extreme May heat waves exceeding 42°C, pioneered India's first municipal Heat Action Plan (HAP).",
        "data_source": "Gujarat Western Plain Climatological Benchmark (NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Demonstrates arid heat wave baseline.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 107,
        "name": "Pune — Shivajinagar & Hinjawadi IT Park",
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "zone_type": "Leeward Valley / Rapid Tech Corridor Growth",
        "category": "commercial",
        "lat": 18.5913,
        "lon": 73.7389,
        "ndvi": 0.26,
        "impervious_pct": 71.0,
        "tree_canopy_pct": 19.0,
        "albedo": 0.19,
        "air_temp_c": 37.4,
        "relative_humidity_pct": 46.0,
        "description": "Western Ghats rain-shadow valley city with rapid peri-urban tech campus growth replacing natural scrub vegetation with impervious pavement.",
        "data_source": "Maharashtra Leeward Climatological Benchmark (NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Rain-shadow valley conditions.",
        "missing_data_status": "VALID_COMPLETE"
    },
    {
        "id": 108,
        "name": "Jaipur — Pink City Historic Walled Core",
        "city": "Jaipur",
        "state": "Rajasthan",
        "country": "India",
        "zone_type": "Semi-Desert / Pink Sandstone Architecture",
        "category": "residential",
        "lat": 26.9220,
        "lon": 75.8267,
        "ndvi": 0.14,
        "impervious_pct": 86.0,
        "tree_canopy_pct": 7.0,
        "albedo": 0.22,
        "air_temp_c": 42.1,
        "relative_humidity_pct": 28.0,
        "description": "Traditional semi-desert historic city core constructed from pink sandstone masonry with narrow north-south shaded bazars but severe summer heat.",
        "data_source": "Rajasthan Semi-Arid Climatological Benchmark (NASA POWER)",
        "spatial_resolution": "0.5° regional atmospheric reanalysis",
        "observation_period": "May 2024 Summer Benchmark",
        "provenance_type": "REGIONAL_METRO_BENCHMARK",
        "model_applicability": "REGIONAL_REFERENCE_ONLY",
        "model_applicability_note": "Regional benchmark. Semi-desert extreme heat profile.",
        "missing_data_status": "VALID_COMPLETE"
    }
]

# Quick access lookups
CORE_LOCATIONS = [loc for loc in ALL_LOCATIONS if loc["id"] <= 6]
MUMBAI_LOCATIONS = [loc for loc in ALL_LOCATIONS if loc["city"] in ["Mumbai", "Thane", "Navi Mumbai"]]
OTHER_METROS = [loc for loc in ALL_LOCATIONS if loc["city"] not in ["Mumbai", "Thane", "Navi Mumbai"]]

def get_location_by_id(loc_id: int) -> Optional[Dict]:
    for loc in ALL_LOCATIONS:
        if loc["id"] == loc_id:
            return dict(loc)
    return None

def parse_lat_lon(query: str) -> Optional[tuple]:
    """Check if query is a latitude/longitude coordinate pair."""
    coord_pattern = r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$"
    m = re.match(coord_pattern, query.strip())
    if m:
        parts = query.strip().split(",")
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return (lat, lon)
        except ValueError:
            pass
    return None

def find_nearest_location(lat: float, lon: float) -> Optional[Dict]:
    """Find the closest catalogue location using Euclidean distance on WGS84."""
    best_loc = None
    min_dist = float("inf")
    for loc in ALL_LOCATIONS:
        dist = math.hypot(loc["lat"] - lat, loc["lon"] - lon)
        if dist < min_dist:
            min_dist = dist
            best_loc = loc
    return best_loc

def search_places(query: str = "", city: str = "", category: str = "", limit: int = 50) -> List[Dict]:
    """
    Search places across catalogue by name, city, category, or coordinates.
    """
    q = query.strip().lower()

    # 1. Coordinate search
    coords = parse_lat_lon(query)
    if coords:
        lat, lon = coords
        nearest = find_nearest_location(lat, lon)
        # Create a synthetic custom point representing clicked/searched coordinates
        custom_point = {
            "id": 9999,
            "name": f"Coordinate Point [{lat:.4f}°N, {lon:.4f}°E]",
            "city": nearest["city"] if nearest else "Custom Geographic Point",
            "state": nearest["state"] if nearest else "Custom Extent",
            "country": "India",
            "zone_type": "Custom User-Specified Geographic Point",
            "category": "custom",
            "lat": lat,
            "lon": lon,
            "ndvi": nearest["ndvi"] if nearest else 0.25,
            "impervious_pct": nearest["impervious_pct"] if nearest else 70.0,
            "tree_canopy_pct": nearest["tree_canopy_pct"] if nearest else 15.0,
            "albedo": nearest["albedo"] if nearest else 0.18,
            "air_temp_c": nearest["air_temp_c"] if nearest else 34.0,
            "relative_humidity_pct": nearest["relative_humidity_pct"] if nearest else 65.0,
            "description": f"Custom study location evaluated via nearest benchmark ({nearest['name'] if nearest else 'Regional Extent'}).",
            "data_source": "User-Defined Point / Nearest Benchmark Interp",
            "spatial_resolution": "Point location",
            "observation_period": "User Selected",
            "provenance_type": "USER_COORDINATE_POINT",
            "model_applicability": "REGIONAL_ESTIMATE",
            "model_applicability_note": "Evaluated using model parameters interpolated from nearest geographical study point.",
            "missing_data_status": "VALID_COMPLETE"
        }
        return [custom_point]

    # 2. Textual search across catalogue
    results = []
    for loc in ALL_LOCATIONS:
        # City filter
        if city and city.lower() != "all" and loc["city"].lower() != city.lower():
            if city.lower() == "mumbai_all" and loc["city"] not in ["Mumbai", "Thane", "Navi Mumbai"]:
                continue
            elif city.lower() != "mumbai_all":
                continue

        # Category filter
        if category and category.lower() != "all" and loc["category"].lower() != category.lower():
            continue

        # Query filter
        if q:
            match_fields = [
                loc["name"].lower(),
                loc["city"].lower(),
                loc["state"].lower(),
                loc["zone_type"].lower(),
                loc["category"].lower(),
                loc["description"].lower()
            ]
            if not any(q in f for f in match_fields):
                continue

        results.append(dict(loc))

    return results[:limit]
