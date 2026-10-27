"""
HeatLens AI — Authoritative Remote Sensing & Environmental Data Catalogue
Defines products, authoritative agencies, physical variables, access protocols,
quality masking rules, and scientific limitations.
"""

from typing import Dict, List

ENVIRONMENTAL_PRODUCTS: List[Dict] = [
    {
        "product_id": "nasa_power_meteorology",
        "name": "NASA POWER Daily Meteorology & Solar Assimilation",
        "agency": "NASA Langley Research Center",
        "division": "Atmospheric Science Data Center (ASDC)",
        "source_models": "GMAO MERRA-2 Atmospheric Reanalysis & CERES/GEWEX Solar Flux Assimilation",
        "official_url": "https://power.larc.nasa.gov/",
        "api_docs_url": "https://power.larc.nasa.gov/docs/",
        "license": "NASA Open Data Policy (Public Domain, Free Academic Use)",
        "spatial_resolution": "0.5° × 0.625° latitude/longitude (~50 km cell)",
        "temporal_resolution": "Daily aggregate / Multi-year archive (1981–present)",
        "study_extent": "Mumbai Metropolitan Center (19.0760°N, 72.8777°E)",
        "coverage_period": "May 1, 2024 to May 31, 2024 (31 validated days, 0 missing)",
        "variables": [
            {"code": "T2M", "name": "2-meter Air Temperature", "units": "°C", "definition": "Arithmetic mean 24-hour ambient air temperature at 2m above ground level."},
            {"code": "T2M_MAX", "name": "Maximum Daily 2m Air Temperature", "units": "°C", "definition": "Peak daytime maximum 2m air temperature."},
            {"code": "T2M_MIN", "name": "Minimum Daily 2m Air Temperature", "units": "°C", "definition": "Lowest nocturnal minimum 2m air temperature."},
            {"code": "RH2M", "name": "2-meter Relative Humidity", "units": "%", "definition": "Ratio of actual water vapor pressure to saturation vapor pressure at 2m."},
            {"code": "ALLSKY_SFC_SW_DWN", "name": "All-Sky Surface Downward Solar Irradiance", "units": "MJ/m²/day", "definition": "Total incoming shortwave solar radiation arriving at the Earth surface."},
            {"code": "WS2M", "name": "2-meter Wind Speed", "units": "m/s", "definition": "Mean daily horizontal atmospheric wind speed at 2m height."}
        ],
        "quality_screening": "Sentinel values (-999.0) screened; range validation enforced (-20°C to 60°C).",
        "scientific_distinction": "Gridded regional atmospheric boundary conditions. Represents regional synoptic weather patterns, NOT direct hyper-local neighborhood street-corner thermometers or satellite radiometric skin LST.",
        "status": "INGESTED_AND_VALIDATED"
    },
    {
        "product_id": "usgs_landsat_st",
        "name": "USGS Landsat 8 & 9 Collection 2 (Level-2 Surface Temperature)",
        "agency": "United States Geological Survey (USGS) & NASA",
        "division": "Earth Resources Observation and Science (EROS) Center",
        "sensor": "Thermal Infrared Sensor 2 (TIRS-2), Band 10 (10.60–11.19 µm)",
        "official_url": "https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature",
        "data_portal": "https://earthexplorer.usgs.gov/",
        "license": "USGS / NASA Open Data Policy (Public Domain)",
        "spatial_resolution": "100m native thermal acquisition, resampled by USGS to 30m UTM grid",
        "temporal_resolution": "16-day revisit per satellite (8-day combined offset in sun-synchronous orbit, ~10:00–10:30 AM local equator crossing)",
        "conversion_formula": "ST (K) = DN × 0.00341802 + 149.0 | ST (°C) = ST (K) − 273.15",
        "quality_masking": "Must filter pixels using QA_PIXEL bitmask (cloud, cloud shadow, cirrus, dilated cloud) and screen using ST_QA uncertainty band (< 2.0 K).",
        "limitations": "Measures radiometric skin temperature of uppermost surface layer, not 2m ambient air temperature. Band 11 is excluded from operational Level-2 ST due to calibration instability. Requires clear-sky conditions.",
        "status": "DOCUMENTED_ROADMAP_SPECIFICATION"
    },
    {
        "product_id": "esa_sentinel2_msi",
        "name": "Copernicus Sentinel-2 Multi-Spectral Instrument (Level-2A)",
        "agency": "European Space Agency (ESA) Copernicus Programme",
        "sensor": "Multi-Spectral Instrument (MSI)",
        "product_level": "Level-2A Bottom-Of-Atmosphere (BOA) Surface Reflectance",
        "official_url": "https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi",
        "data_portal": "https://dataspace.copernicus.eu/",
        "license": "Copernicus Open Access Policy (Free and Open)",
        "spatial_resolution": "10m for Bands 2, 3, 4, 8; 20m for Red-Edge and SWIR Bands 11, 12",
        "temporal_resolution": "5-day constellation revisit (Sentinel-2A & 2B combined)",
        "indices": [
            {"code": "NDVI", "formula": "(Band 8 [NIR] − Band 4 [Red]) / (Band 8 + Band 4)", "resolution": "10m", "interpretation": "2D optical greenness and chlorophyll density."},
            {"code": "NDBI", "formula": "(Band 11 [SWIR] − Band 8 [NIR]) / (Band 11 + Band 8)", "resolution": "20m", "interpretation": "Built-up and impervious surface indicator."}
        ],
        "reflectance_scale": "Integer DN scaled by 1/10000",
        "limitations": "NDVI quantifies 2D photosynthetic vigor, NOT physical 3D canopy height or volumetric tree biomass. Deriving canopy cover percentage requires empirical calibration against aerial LiDAR or high-resolution land-cover baselines.",
        "status": "DOCUMENTED_ROADMAP_SPECIFICATION"
    },
    {
        "product_id": "nasa_ecostress",
        "name": "NASA ECOSTRESS (ISS Thermal Radiometer)",
        "agency": "NASA Jet Propulsion Laboratory (JPL)",
        "platform": "International Space Station (ISS)",
        "sensor": "Multispectral Thermal Infrared Radiometer (5 thermal bands, 8.29–12.09 µm)",
        "core_product": "ECO2LSTE (Temperature and Emissivity Separation TES algorithm)",
        "official_url": "https://ecostress.jpl.nasa.gov/",
        "data_portal": "https://lpdaac.usgs.gov/products/eco2lstev002/",
        "license": "NASA Open Data Policy (Public Domain)",
        "spatial_resolution": "70m gridded resolution (38m × 69m native resolution at nadir)",
        "orbital_characteristics": "Precessing, non-sun-synchronous inclined orbit (51.6°). Captures diurnal urban heat inertia and plant water stress across varying times of day and night.",
        "revisit_interval": "Irregular 1 to 5 days depending on ISS trajectory",
        "limitations": "Restricted to clear-sky conditions, coverage geographically bounded between 52°N and 52°S latitudes.",
        "status": "DOCUMENTED_ROADMAP_SPECIFICATION"
    },
    {
        "product_id": "esa_worldcover",
        "name": "ESA WorldCover 10m Global Land Cover",
        "agency": "European Space Agency (ESA) & VITO Remote Sensing",
        "official_url": "https://esa-worldcover.org/",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
        "spatial_resolution": "10m global raster",
        "classes": "11 discrete land cover categories (Tree cover, Shrubland, Grassland, Cropland, Built-up, Bare vegetation, Water bodies, Wetland, Mangroves, Moss/lichen, Snow/ice).",
        "application": "Directly derives urban impervious surface percentage and tree canopy percentage at 10m grid cell resolution.",
        "status": "DOCUMENTED_ROADMAP_SPECIFICATION"
    }
]

def get_product_catalogue() -> List[Dict]:
    return ENVIRONMENTAL_PRODUCTS
