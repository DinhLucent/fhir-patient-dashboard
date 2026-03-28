# fhir-patient-dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?logo=flask)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-orange?logo=chartdotjs)
![License](https://img.shields.io/badge/License-MIT-green)

A professional full-stack clinical dashboard for visualizing patient vitals and health trends using FHIR R4 data. It provides an interactive interface for practitioners to monitor population health metrics and individual patient histories.

## Key Features

- **FHIR R4 Native**: Parses complex FHIR Bundles containing Patients and Observations into display-ready models.
- **Interactive Vitals**: Dynamic line charts for Heart Rate, Body Temperature, and Blood Glucose using Chart.js.
- **Population Analytics**: Built-in API for aggregating clinical KPIs (Average Age, Average Heart Rate) across patient cohorts.
- **Optimized Frontend**: Advanced client-side caching of clinical data to ensure a lag-free user experience.
- **Glassmorphism UI**: Modern, clinical-grade design system with responsive layouts and "Outfit" typography.

## Quick Start

### Run the dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python -m fhir_dashboard.app
```

Navigate to `http://localhost:5000` to view the interactive dashboard.

## API Documentation

### `GET /api/patients`
Returns a list of all patients and their associated observations in a flattened, easy-to-chart format.

### `GET /api/stats`
Returns population-level metrics:
```json
{
  "count": 25,
  "avg_age": 42.5,
  "avg_heart_rate": 72.4,
  "vitals_recorded": 450
}
```

## How it works — module by module

### `fhir_dashboard/parser.py` — The FHIR Engine

Converts nested FHIR JSON (Resources & Bundles) into lightweight Python dataclasses. It handles ISO 8601 timestamps and maps clinical codes to display names.

### `static/js/dashboard.js` — Data Flow Orchestrator

Implements a single-fetch data management pattern. It retrieves clinical data once at startup and performs all patient switching and filtering in-memory for instant feedback.

## Project Structure

```
fhir-patient-dashboard/
├── fhir_dashboard/         # Backend (Flask)
│   ├── app.py              # API Routes and Orchestration
│   ├── models.py           # Patient & Observation Dataclasses
│   └── parser.py           # FHIR Transformation Logic
├── static/                 # CSS & JS assets
├── templates/              # HTML Templates (Jinja2)
├── data/                   # Sample FHIR JSON bundles
├── tests/                  # Backend unit tests
├── requirements.txt
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/DinhLucent/fhir-patient-dashboard.git
cd fhir-patient-dashboard
pip install -r requirements.txt
```

## License

MIT License — see [LICENSE](LICENSE)

---
Built by [DinhLucent](https://github.com/DinhLucent)
