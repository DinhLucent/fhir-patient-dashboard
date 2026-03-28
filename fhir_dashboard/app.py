"""
FHIR Dashboard App — Serves the interactive patient data visualization.
"""

import json
from pathlib import Path
from flask import Flask, render_template, jsonify

from fhir_dashboard.parser import FHIRParser

app = Flask(__name__, 
            template_folder="../templates", 
            static_folder="../static")

# Sample data path
DATA_FILE = Path(__file__).parent.parent / "data" / "patient_bundle.json"

def get_patients():
    """Load and parse sample FHIR data."""
    if not DATA_FILE.exists():
        return []
    
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
        return FHIRParser.parse_bundle(data)

@app.route("/")
def index():
    """Render main dashboard."""
    patients = get_patients()
    return render_template("index.html", patients=patients)

@app.route("/api/patients")
def api_patients():
    """Return patient data as JSON."""
    patients = get_patients()
    # Simplified JSON for frontend charts
    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "observations": [
                {
                    "display": o.display,
                    "value": o.value,
                    "unit": o.unit,
                    "time": o.timestamp.isoformat()
                } for o in p.observations
            ]
        })
    return jsonify(result)


@app.route("/api/stats")
def api_stats():
    """Return population-level statistics."""
    patients = get_patients()
    if not patients:
        return jsonify({})
    
    all_obs = []
    for p in patients:
        all_obs.extend(p.observations)
    
    stats = {
        "count": len(patients),
        "avg_age": sum(p.age for p in patients) / len(patients),
        "vitals_recorded": len(all_obs),
        "heart_rates": [o.value for o in all_obs if o.display == "Heart rate"]
    }
    
    if stats["heart_rates"]:
        stats["avg_heart_rate"] = sum(stats["heart_rates"]) / len(stats["heart_rates"])
    
    return jsonify(stats)


@app.route("/api/stats")
def api_stats():
    """Return population-level statistics."""
    patients = get_patients()
    if not patients:
        return jsonify({})
    
    all_obs = []
    for p in patients:
        all_obs.extend(p.observations)
    
    stats = {
        "count": len(patients),
        "avg_age": sum(p.age for p in patients) / len(patients),
        "vitals_recorded": len(all_obs),
        "heart_rates": [o.value for o in all_obs if o.display == "Heart rate"]
    }
    
    if stats["heart_rates"]:
        stats["avg_heart_rate"] = sum(stats["heart_rates"]) / len(stats["heart_rates"])
    
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
