import csv, json, math, os
from string import Template

BASE = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE, "jura_validation_set.csv")

METALS = ["Cd","Cu","Pb","Co","Cr","Ni","Zn"]
COLORS = ["#f72585","#7209b7","#3a0ca3","#4361ee","#4cc9f0","#06d6a0","#ffd166"]

rows = []
with open(csv_path, newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for line in reader:
        if len(line) < 12 or line[0].strip() == "":
            continue
        try:
            def clean(val): return float(val.replace(',', '.').replace('/.', '.').replace('..', '.'))
            rows.append({
                "id": int(clean(line[0])), "x": clean(line[1]), "y": clean(line[2]),
                "rock": int(clean(line[3])), "land": int(clean(line[4])),
                "Cd": clean(line[5]), "Cu": clean(line[6]), "Pb": clean(line[7]),
                "Co": clean(line[8]), "Cr": clean(line[9]),
                "Ni": clean(line[10]), "Zn": clean(line[11]),
            })
        except Exception as e:
            pass

n = len(rows)

TMPL = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Validation Set &mdash; Live Geographic Maps (n=$n_samples)</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#0f0f1a;color:#e0e0ff;min-height:100vh}
header{background:linear-gradient(135deg,#1a1a3e 0%,#0d0d2b 100%);padding:28px 40px;border-bottom:1px solid #2a2a5a;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.logo{font-size:2rem}
.header-text h1{font-size:1.6rem;font-weight:700;background:linear-gradient(90deg,#4cc9f0,#7209b7);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header-text p{font-size:.85rem;color:#8888bb;margin-top:4px}
.nav-group{display:flex;gap:12px;margin-left:auto;align-items:center}
.badge{background:rgba(76,201,240,.15);border:1px solid #4cc9f0;color:#4cc9f0;border-radius:20px;padding:4px 14px;font-size:.78rem;font-weight:600}
.nav-btn{background:rgba(76,201,240,.1);border:1px solid #4cc9f0;color:#4cc9f0;border-radius:8px;padding:6px 14px;font-size:.85rem;font-weight:600;text-decoration:none;transition:all 0.2s}
.nav-btn.primary{background:#4cc9f0;color:#0d0d2b;border-color:#4cc9f0}
.nav-btn:hover{background:rgba(76,201,240,.25)}
.nav-btn.primary:hover{opacity:0.8}
main{padding:32px 40px;max-width:1800px;margin:0 auto}

/* Filter Panel CSS */
.filter-panel { background:#13132b; border:1px solid #2a2a5a; border-radius:14px; padding:20px 24px; margin-bottom:24px; display:flex; gap:36px; flex-wrap:wrap; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.filter-group { display:flex; gap:16px; align-items:center; flex-wrap:wrap;}
.filter-group strong { color:#4cc9f0; font-size:.85rem; text-transform:uppercase; letter-spacing:1px; margin-right:4px; }
.filter-group label { color:#a0a0cc; font-size:.85rem; display:flex; gap:6px; align-items:center; cursor:pointer; transition:color 0.2s; }
.filter-group label:hover { color:#e0e0ff; }
.filter-group input { cursor:pointer; accent-color:#f72585; width:16px; height:16px; }

.grid-maps{display:flex;flex-wrap:wrap;gap:24px;justify-content:center}
.card{background:#13132b; border:1px solid #2a2a5a; border-radius:14px; padding:24px; width:calc(50% - 12px); min-width:400px; flex-grow:1}
.card-title{font-size:1rem;font-weight:600;color:#8888cc;margin-bottom:16px;text-transform:uppercase;letter-spacing:.5px;display:flex;align-items:center;justify-content:space-between}
.metal-range{font-size:0.75rem;font-weight:400;color:#e0e0ff;background:#2a2a5a;padding:4px 8px;border-radius:6px}
.leaflet-container {height: 400px; border-radius: 8px; z-index: 1;}
.leaflet-popup-content-wrapper {background:#1a1a3e; color:#e0e0ff; border:1px solid #3a3a6a; border-radius:6px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);}
.leaflet-popup-tip {background:#1a1a3e;}
footer{text-align:center;padding:24px;color:#444466;font-size:.78rem;border-top:1px solid #1a1a3a}
</style>
</head>
<body>
<header>
  <div class="logo">&#127757;</div>
  <div class="header-text">
    <h1>Live Geographic Maps (WGS84) &mdash; Live Filtering</h1>
    <p>Validation Set &middot; 7 Heavy Metals &middot; Projected on OpenStreetMap Topology</p>
  </div>
  <div class="nav-group">
    <div class="badge">n = $n_samples samples</div>
    <a href="index2.html" class="nav-btn">&larr; Back to EDA</a>
    <a href="../Prediction set/prediction_maps.html" class="nav-btn">&larr; Prediction Maps</a>
  </div>
</header>
<main>
  
  <div class="filter-panel">
    <div class="filter-group">
      <strong>Rock Type:</strong>
      <label><input type="checkbox" class="filter-cb" data-type="rock" value="1" checked> Argovian</label>
      <label><input type="checkbox" class="filter-cb" data-type="rock" value="2" checked> Kimmeridgian</label>
      <label><input type="checkbox" class="filter-cb" data-type="rock" value="3" checked> Sequanian</label>
      <label><input type="checkbox" class="filter-cb" data-type="rock" value="4" checked> Portlandian</label>
      <label><input type="checkbox" class="filter-cb" data-type="rock" value="5" checked> Quaternary</label>
    </div>
    <div class="filter-group">
      <strong>Land Use:</strong>
      <label><input type="checkbox" class="filter-cb" data-type="land" value="1" checked> Forest</label>
      <label><input type="checkbox" class="filter-cb" data-type="land" value="2" checked> Pasture</label>
      <label><input type="checkbox" class="filter-cb" data-type="land" value="3" checked> Meadow</label>
      <label><input type="checkbox" class="filter-cb" data-type="land" value="4" checked> Tillage</label>
    </div>
  </div>

  <div class="grid-maps" id="mapsGrid"></div>
</main>
<footer>Jura Spatial Maps &middot; Swiss Jura Heavy Metals Dataset &middot; Validation Set (n=$n_samples)</footer>
<script>
var ROWS = $rows_js;
var METALS = $metals_js;

// Utility functions
function lerp(a,b,t){return a+(b-a)*t;}
function metalColor(val,mn,mx){
  var t=Math.max(0,Math.min(1,(val-mn)/(mx-mn)));
  var r=Math.round(lerp(14,247,t)),g=Math.round(lerp(165,37,t)),b=Math.round(lerp(233,133,t));
  return 'rgb('+r+','+g+','+b+')';
}

// Convert Local grid (km) to approximate Lat/Lon (WGS84)
function projectWGS84(x_km, y_km) {
  var lat_origin = 47.15;
  var lon_origin = 6.85;
  var lat = lat_origin + (y_km * (1 / 111.32));
  var lon = lon_origin + (x_km * (1 / (111.32 * Math.cos(lat_origin * Math.PI / 180))));
  return [lat, lon];
}

var grid = document.getElementById('mapsGrid');
var ALL_MARKERS = []; // Store references for filtering

METALS.forEach(function(m){
  var vals = ROWS.map(function(r){return r[m];});
  var mn = Math.min.apply(null, vals), mx = Math.max.apply(null, vals);
  
  var card = document.createElement('div');
  card.className = 'card';
  card.innerHTML = '<div class="card-title">' + m + ' (ppm) <span class="metal-range">Range: ' + mn.toFixed(2) + ' &rarr; ' + mx.toFixed(2) + '</span></div><div id="map_' + m + '"></div>';
  grid.appendChild(card);
  
  var map = L.map('map_' + m);
  
  // Custom Dark Mode Map Tiles via CartoDB
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18
  }).addTo(map);

  var latLngs = [];
  
  ROWS.forEach(function(r) {
      var ll = projectWGS84(r.x, r.y);
      latLngs.push(ll);
      
      var color = metalColor(r[m], mn, mx);
      
      var circle = L.circleMarker(ll, {
          radius: 6,
          fillColor: color,
          color: '#ffffff',
          weight: 1.2,
          opacity: 0.9,
          fillOpacity: 0.85
      }).addTo(map);
      
      var rStr = ['Argovian','Kimmeridgian','Sequanian','Portlandian','Quaternary'][r.rock-1];
      var lStr = ['Forest','Pasture','Meadow','Tillage'][r.land-1];

      var popupContent = '<b>Validation ID: ' + r.id + '</b><hr style="border:0;border-top:1px solid #3a3a6a;margin:6px 0;">' + 
                         m + ' Conc: <b style="color:#4cc9f0">' + r[m] + ' ppm</b><br>' + 
                         'Rock Type: <b>' + rStr + '</b><br>' + 
                         'Land Use: <b>' + lStr + '</b><br>' + 
                         '<span style="color:#888;font-size:0.8em;display:block;margin-top:4px;">Grid: (' + r.x + 'km, ' + r.y + 'km)</span>';
      circle.bindPopup(popupContent);
      
      // Optional tooltip for fast hovering
      circle.bindTooltip(r[m].toString(), {direction:'top', className:'map-tooltip'});

      ALL_MARKERS.push({marker: circle, rock: r.rock, land: r.land});
  });

  // Fit view bounds to data natively
  map.fitBounds(L.latLngBounds(latLngs), {padding: [15, 15]});
});

// Live Filtering Engine
function applyFilters() {
    var checkedRocks = Array.from(document.querySelectorAll('.filter-cb[data-type="rock"]:checked')).map(cb => parseInt(cb.value));
    var checkedLands = Array.from(document.querySelectorAll('.filter-cb[data-type="land"]:checked')).map(cb => parseInt(cb.value));
    
    ALL_MARKERS.forEach(function(item) {
        var isVisible = checkedRocks.includes(item.rock) && checkedLands.includes(item.land);
        if (isVisible) {
            item.marker.setStyle({opacity: 0.9, fillOpacity: 0.85});
            item.marker.bringToFront(); // Ensure visible points are clickable
        } else {
            item.marker.setStyle({opacity: 0, fillOpacity: 0});
            item.marker.closePopup(); // close if it was open
        }
    });
}
document.querySelectorAll('.filter-cb').forEach(cb => cb.addEventListener('change', applyFilters));

</script>
<style>
.map-tooltip {background:#1a1a3e; border:1px solid #4cc9f0; color:#e0e0ff; font-weight:600;}
.map-tooltip.leaflet-tooltip-top:before {border-top-color:#4cc9f0;}
</style>
</body>
</html>
""")

out = os.path.join(BASE, "validation_maps.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(TMPL.substitute(
        n_samples=n,
        rows_js=json.dumps(rows),
        metals_js=json.dumps(METALS)
    ))

print(f"Validation Maps Dashboard (Filtered) written -> {out}")
