# FHIR Patient Dashboard

A modern, responsive dashboard for visualizing medical patient data in FHIR R4 format.

## Features

- **FHIR R4 Parsing**: Built-in parser for Patient and Observation resources.
- **Interactive UI**: Real-time vital signs monitoring charts (Heart Rate, BP, Glucose).
- **Glassmorphism Design**: Sleek, modern aesthetic using pure CSS.
- **REST API**: Flask-based API for programmatic data access.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: Vanilla CSS (Glassmorphism), Chart.js
- **Data**: FHIR R4 JSON

## Quick Start

```bash
pip install -e .
python fhir_dashboard/app.py
```
Then visit `http://127.0.0.1:5000` in your browser.

## License

MIT
