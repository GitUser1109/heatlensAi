# Real Satellite & Geospatial Data Integration Roadmap
**HeatLens AI — Environmental Decision Support System**

> **Scientific Integrity & System Separation Notice:** 
> HeatLens AI operates with a strict, transparent separation between two distinct data systems:
> 1. **Observed Environmental Meteorological Baseline:** Real, gridded atmospheric reanalysis data for Mumbai (May 1–31, 2024) ingested from NASA POWER (GMAO MERRA-2 and CERES/GEWEX solar assimilation). These are synoptic regional boundary conditions on a 0.5° × 0.625° grid (~50 km cell), *not* micro-urban ground thermometers at specific street intersections or satellite radiometric skin Land Surface Temperature (LST).
> 2. **Synthetic Machine-Learning Demonstration:** An ensemble of 220 decorrelated decision trees trained on 1,800 synthetic Mumbai study samples to demonstrate non-linear multi-factor sensitivity (NDVI, tree canopy %, impervious surface %, albedo, background air temp, humidity). The predicted 0–100 score is an illustrative unitless relative risk index—it is *not* a measured Celsius temperature or a validated municipal heat forecast.

---

## 1. Authoritative Remote Sensing Data Providers & Satellite Sensors

### A. USGS Landsat 8 & 9 Collection 2 (Level-2 Surface Temperature)
- **Authoritative Provider:** United States Geological Survey (USGS) & NASA Earth Resources Observation and Science (EROS) Center.
- **Sensor:** Thermal Infrared Sensor 2 (TIRS-2), Band 10 (10.60–11.19 µm). *(Note: Band 11 is not used for quantitative operational Level-2 ST due to larger calibration uncertainty).*
- **Spatial Resolution:** 100 m native thermal resolution, resampled by USGS to a 30 m grid.
- **Temporal Repeat Cycle:** 16-day revisit per satellite (8-day offset with Landsat 8 and 9 combined in sun-synchronous orbit, ~10:00–10:30 AM local equator crossing).
- **Physical Variable:** Radiometric Land Surface Temperature (LST) in Kelvin, measuring emitted skin temperature.
- **Product-Specific Scale Factor & Conversion Formula:**
  $$\text{ST (Kelvin)} = \text{DN} \times 0.00341802 + 149.0$$
  $$\text{ST (°C)} = \text{ST (Kelvin)} - 273.15$$
  *(Where $\text{DN}$ represents the 16-bit integer Digital Number stored in the `ST_B10` raster).*
- **Quality Flags & QA Masking:** Must filter pixels using the `QA_PIXEL` bitmask (filtering bits for cloud, cloud shadow, cirrus, dilated cloud) and screen using the `ST_QA` (Surface Temperature Quality Assessment) atmospheric uncertainty band (acceptable uncertainty typically $< 2.0\text{ K}$).
- **Authoritative Documentation:** [USGS Landsat Collection 2 Surface Temperature](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature) | [USGS EarthExplorer](https://earthexplorer.usgs.gov/).

### B. Copernicus Sentinel-2 Multi-Spectral Instrument (MSI) Level-2A
- **Authoritative Provider:** European Space Agency (ESA) Copernicus Programme.
- **Sensor:** Multi-Spectral Instrument (MSI), Level-2A Bottom-Of-Atmosphere (BOA) surface reflectance.
- **Spatial Resolution:** 10 m for Band 8 (NIR, 842 nm) and Band 4 (Red, 665 nm); 20 m for Red-Edge and Short-Wave Infrared (SWIR Band 11 and Band 12).
- **Reflectance Scaling:** Stored integer DN values scaled by $1/10000$ to obtain true surface reflectance $[0.0, 1.0]$.
- **Calculated Environmental Indices:**
  - **NDVI (Normalized Difference Vegetation Index):**
    $$\text{NDVI} = \frac{\text{Band 8 (NIR)} - \text{Band 4 (Red)}}{\text{Band 8 (NIR)} + \text{Band 4 (Red)}}$$
  - **NDBI (Normalized Difference Built-up Index):**
    $$\text{NDBI} = \frac{\text{Band 11 (SWIR 20m)} - \text{Band 8 (NIR 10m)}}{\text{Band 11 (SWIR 20m)} + \text{Band 8 (NIR 10m)}}$$
- **Scientific Limitations:** NDVI is a 2D optical spectral index measuring chlorophyll absorption in the red band and cell-structure scattering in the near-infrared. It does **not** directly measure physical 3D canopy height or volumetric tree canopy fraction. Deriving canopy cover percentage requires empirical calibration against aerial LiDAR, UAV photogrammetry, or high-resolution land-cover baselines (e.g., ESA WorldCover 10m).
- **Authoritative Documentation:** [ESA Copernicus Sentinel-2 MSI User Guide](https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi) | [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/).

### C. NASA ECOSTRESS (ISS Radiometer)
- **Authoritative Provider:** NASA Jet Propulsion Laboratory (JPL) & LP DAAC.
- **Sensor:** Prototype multispectral thermal infrared radiometer aboard the International Space Station (ISS) across 5 thermal infrared bands (8.29–12.09 µm).
- **Spatial Resolution:** 70 m gridded resolution ($38\text{ m} \times 69\text{ m}$ native resolution at nadir).
- **Core Thermal Product:** `ECO2LSTE` utilizing the Temperature and Emissivity Separation (TES) algorithm.
- **Orbital Sampling & Diurnal Capability:** Mounted on the ISS in an inclined ($51.6^\circ$), precessing non-sun-synchronous orbit. Unlike sun-synchronous satellites (Landsat/Sentinel) that pass at the same local morning hour, ECOSTRESS samples the Earth at varying times of day and night over revisit intervals of 1 to 5 days, enabling empirical quantification of diurnal urban thermal inertia and evaporative stress.
- **Scientific Limitations:** Restricted to clear-sky conditions, irregular revisit cadence, and spatial coverage strictly bounded between latitudes 52°N and 52°S.
- **Authoritative Documentation:** [NASA JPL ECOSTRESS Portal](https://ecostress.jpl.nasa.gov/) | [NASA Earthdata LP DAAC](https://lpdaac.usgs.gov/products/eco2lstev002/).

### D. NASA POWER (Prediction of Worldwide Energy Resources)
- **Authoritative Provider:** NASA Langley Research Center POWER Project.
- **Product Provenance:** Derived from GMAO MERRA-2 (Modern-Era Retrospective analysis for Research and Applications, Version 2) atmospheric assimilation and satellite-observed solar fluxes (CERES / GEWEX).
- **Spatial Resolution:** Gridded $0.5^\circ \times 0.625^\circ$ latitude/longitude resolution (~50 km grid cell).
- **Study Location:** Mumbai Metropolitan Center (19.0760°N, 72.8777°E).
- **Temporal Observation Window:** May 1, 2024 to May 31, 2024 (31 consecutive daily records, 0 missing).
- **Specific Variables & Physical Units:**
  - `T2M`: Daily mean air temperature at 2 meters above ground (°C).
  - `T2M_MAX`: Maximum daily air temperature at 2 meters above ground (°C).
  - `T2M_MIN`: Minimum daily air temperature at 2 meters above ground (°C).
  - `RH2M`: Daily mean relative humidity at 2 meters above ground (%).
  - `ALLSKY_SFC_SW_DWN`: All-sky surface downward shortwave solar irradiance ($\text{MJ/m}^2/\text{day}$).
  - `WS2M`: Daily mean wind speed at 2 meters above ground ($\text{m/s}$).
- **Calculated & Independently Verified Mumbai Metrics (May 2024):**
  - **Monthly Mean 24h Air Temperature ($T2M$ Mean):** $32.16 ^\circ\text{C}$
  - **Monthly Mean Daily Daytime High ($T2M\_MAX$ Mean):** $39.23 ^\circ\text{C}$
  - **Single-Day Peak Maximum Extreme ($T2M\_MAX$ Peak):** $40.86 ^\circ\text{C}$ (Recorded on **May 5, 2024**)
  - **Single-Day Lowest Minimum Extreme ($T2M\_MIN$ Lowest):** $23.84 ^\circ\text{C}$ (Recorded on **May 3, 2024**)
  - **Monthly Mean Relative Humidity ($RH2M$ Mean):** $59.9 \%$
  - **Mean Solar Surface Irradiance ($ALLSKY\_SFC\_SW\_DWN$ Mean):** $6.83\text{ MJ/m}^2/\text{day}$
  - **Mean Wind Speed ($WS2M$ Mean):** $2.53\text{ m/s}$
- **Crucial Scientific Distinction:** These data represent regional atmospheric boundary conditions derived from assimilated global models and satellite solar irradiance. They do **not** represent local in-situ ground-station thermometers in specific Mumbai streets, nor are they radiometric skin LST.
- **Authoritative Documentation:** [NASA POWER Data Portal](https://power.larc.nasa.gov/) | [API Documentation](https://power.larc.nasa.gov/docs/).

---

## 2. Preventing Data Leakage in Spatial-Temporal ML

Standard machine learning projects routinely apply naive uniform random train/test splits. In geospatial remote sensing, **uniform random sampling causes severe spatial data leakage** due to spatial autocorrelation (Tobler's First Law of Geography: *"Near things are more related than distant things"*).

```
NAIVE RANDOM SPLIT (Severe Data Leakage):
[Pixel A (Train)] [Pixel B (Test)] [Pixel C (Train)]
--> Test pixel B is 30m away from training pixels; the model simply memorizes the local neighborhood rather than learning generalizable biophysical relationships.

DEFENSIBLE SPLIT (Spatial Block Holdout):
+--------------------+--------------------+
|  BLOCK 1 (Train)   |   BLOCK 2 (Test)   |
|  Bandra & Dadar    |   Powai & Vikhroli |
+--------------------+--------------------+
|  BLOCK 3 (Test)    |   BLOCK 4 (Train)  |
|  South Mumbai      |   Thane Suburban   |
+--------------------+--------------------+
```

### Best-Practice Protocols:
1. **Spatial Block Cross-Validation:** Divide the study boundary into $5 \times 5\text{ km}$ spatial grid blocks. Train on a set of blocks and test strictly on unseen, disjoint geographic zones.
2. **Temporal Split:** Train on pre-monsoon summer scenes from one year (e.g., May 2024) and evaluate on May 2025 scenes to verify multi-temporal generalization.
3. **Cloud & Shadow Filtering:** Apply strict pixel-level quality screening (`QA_PIXEL & 0x18 == 0`) to discard cirrus, cloud contamination, and terrain shadowing.

---

## 3. End-to-End Real Data Ingestion Workflow

```mermaid
graph TD
    A["USGS EarthExplorer / Landsat 8-9"] -->|Download GeoTIFF| B["Thermal Band 10 DN"]
    C["Copernicus / Sentinel-2"] -->|Download Level-2A| D["Surface Reflectance B4 & B8"]
    E["NASA POWER API"] -->|REST Request| F["Daily Air Temp & Humidity"]
    
    B -->|Scale: DN * 0.00341802 + 149.0 - 273.15| G["Radiometric LST in Celsius"]
    D -->|Band Math (B8-B4)/(B8+B4)| H["Vegetation Index NDVI"]
    D -->|High-pass Land Classification| I["Impervious % & Canopy %"]
    
    G --> J["Resample & Align to 30m Grid Cells"]
    H --> J
    I --> J
    F --> J
    
    J --> K["Spatial Block Train/Test Split"]
    K --> L["Train Random Forest Regressor"]
    L --> M["Validate Real MAE / RMSE against Baseline"]
```

1. **Acquire Cloud-Free Satellite Scenes:** Retrieve matched Landsat/Sentinel scenes for the study area during clear-sky pre-monsoon conditions (March–May in Mumbai).
2. **Atmospheric Correction & Radiometric Calibration:** Convert Digital Numbers (DN) to Land Surface Temperature using official USGS Collection 2 gain ($0.00341802$) and offset ($149.0$) coefficients.
3. **Band Math & Land Cover Processing:**
   - Compute NDVI from red and near-infrared surface reflectance ($B8, B4$).
   - Extract impervious surface fraction using normalized spectral indices or open High-Resolution Land Cover rasters (e.g., ESA WorldCover 10m).
4. **Zonal Harmonization:** Resample and reproject all layers into a common projected coordinate system (`UTM Zone 43N / WGS 84` for Mumbai) at 30-meter pixel resolution.
5. **Model Retraining:** Execute `scripts/train_model.py` with the extracted real raster points, report spatial cross-validation metrics, and compare against the mean baseline.

---

## 4. Citation and Attribution Guidelines

When publishing or presenting findings derived from these public datasets, cite the primary data archives:
- **USGS Landsat:** U.S. Geological Survey (2020). *Landsat Collection 2 Level 2 Surface Temperature*. DOI: [10.5066/P9OGBGM6](https://doi.org/10.5066/P9OGBGM6).
- **ESA Copernicus:** European Space Agency (2023). *Sentinel-2 MSI Level-2A Surface Reflectance*.
- **NASA ECOSTRESS:** Hulley, G., Hook, S. (2018). *ECOSTRESS Land Surface Temperature and Emissivity Daily L2 Global 70m V002*. NASA EOSDIS Land Processes DAAC. DOI: [10.5067/ECOSTRESS/ECO2LSTE.002](https://doi.org/10.5067/ECOSTRESS/ECO2LSTE.002).
- **NASA POWER:** Sparks, A. H. (2018). *nasapower: A NASA POWER Global Meteorology, Surface Solar Energy and Climatology Data Client*. JOSS, 3(30), 1035. DOI: [10.21105/joss.01035](https://doi.org/10.21105/joss.01035).
