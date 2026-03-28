# Jura Heavy Metals — Validation Set Live Geographic Maps

## Overview

This dashboard (`index.html`) projects the strictly held-out 100-sample validation set from the Swiss Jura geochemical dataset onto **live OpenStreetMap topography** using **Leaflet.js** and a WGS84 affine coordinate transformation. Its primary purpose is **spatial validation** — enabling visual inspection of where model predictions succeed or fail relative to real geographic and geological context.

## Contents of This Folder

| File | Purpose |
|---|---|
| `index.html` | Live geographic map dashboard (open in any browser) |
| `gen_val_maps.py` | Python generator script — re-run to rebuild `index.html` |

> **Note:** The CSV source data lives in `../validation set EDA/jura_validation_set.csv`. The generator reads both the validation and prediction CSVs to compute the shared study boundary polygon.

## Dashboard Features

### 7-Map Grid Layout
Seven independent **Leaflet.js** maps — one per heavy metal (Cd, Cu, Pb, Co, Cr, Ni, Zn) — rendered side-by-side on a dark CARTO basemap. Each map:
- Colour-grades every validation sample from **blue (low)** to **pink/red (high)** concentration
- Auto-zooms to the tight bounding box of the hold-out data on load
- Shows a **clickable popup** on each point with: Validation ID · Concentration (ppm) · Rock Type · Land Use · Grid coordinates

### Live Categorical Filter Panel
A persistent control bar above the maps provides instant filtering across **all 7 maps simultaneously**:

**Rock Type** (ordered youngest → oldest per stratigraphic literature, with age labels):
- Quaternary (~2.58 Ma) · Portlandian (~152 Ma) · Kimmeridgian (~157 Ma) · Sequanian (~163 Ma) · Argovian (~166 Ma)

**Land Use:**
- Forest · Pasture · Meadow · Tillage

Unchecking any category instantly clears those validation points from view across all maps. This enables targeted *geological unit auditing* — e.g. isolating all Argovian rock samples to check if a model systematically underestimates concentrations in the oldest formation.

### Combined Study Area Boundary
A toggleable **dashed golden polygon** overlaid on every map defines the combined study footprint across both the prediction and validation datasets (all 359 points). The boundary is computed as a **convex hull** of all points with a **+500 m outward offset**. On the validation maps, this boundary provides immediate visual confirmation that the 100 hold-out locations are geographically distributed within the broader training zone and not artificially clustered.

## Why Visualise the Validation Set Geographically?
Aggregate metrics (RMSE, R²) can mask systematic spatial failures. A model trained on Kimmeridgian limestone samples may silently fail over Quaternary alluvial deposits. This dashboard makes such geographic biases immediately visible:
1. Filter to a single rock type using the Live Panel
2. Assess whether the remaining validation dots cluster in a specific corner of the study area
3. Correlate with the prediction set maps to identify coverage gaps

## Coordinate Projection Method
Same affine transformation as the prediction map: `WGS84` coordinates derived from local `X/Y km` grid, anchored at Lat 47.15°, Lon 6.85° with cosine-corrected longitude scaling.

## Navigation
- **← Back to EDA** — Returns to the validation statistical analysis dashboard
- **← Prediction Maps** — Opens the equivalent live map for the 259-sample training set
