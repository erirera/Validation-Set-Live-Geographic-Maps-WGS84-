# Geographic Maps Dashboard — Validation Set (n=100)

This directory contains the **Validation Map Viewer** (`validation_maps.html`), specifically isolating the strict 100-sample Swiss Jura hold-out testing set onto a live geographic mapping application.

## 🔬 Evaluating AI on Geography and Categories

Relying strictly on generalized numerical metrics (like RMSE, R², etc.) to score a geospatial machine learning model is a trap. You run the risk of immense "Spatial Leakage" or missing systemic failures in particular geological categories.

This dashboard actively remedies this by mapping your specific 100 Validation samples perfectly across 7 independent, fully interactive **Leaflet.js OpenStreetMap** layouts. 

### The AI Evaluation Strategy

1. **Spotting Geographic Failures**: Simply mapping your algorithm's test predictions onto a live topographical layout can reveal if your model only succeeds in southern elevations or valleys, but universally fails globally.
2. **Dynamic Categorical Isolation**: Using the powerful **Live Switchboard Panel** at the top of the interface, you can instantly uncheck combinations of "Rock Types" and "Land Uses." 
   *Did your Kriging algorithm break down solely on Argovian Rock? Uncheck all other geologic types and look at the isolated hold-out map in seconds to visually audit your model's weak points.*
3. **Sparsity Mapping**: Real-world topographical scaling visually guarantees your holdout sample accurately and fairly represents the broader training zone without severe clustering.

## 🔗 Integrated Workflow
1. Use the main header to swap back linearly out of the maps into the core statistical Validation statistics interface (`index2.html`).
2. Alternatively, instantly cross-reference density with the primary predictive maps (`prediction_maps.html`).
