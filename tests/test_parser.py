import json
from datetime import date
from fhir_dashboard.parser import FHIRParser

def test_parse_patient():
    patient_json = {
        "resourceType": "Patient",
        "id": "123",
        "name": [{"family": "Smith", "given": ["Alice"]}],
        "gender": "female",
        "birthDate": "1990-05-20"
    }
    patient = FHIRParser.parse_patient(patient_json)
    assert patient.id == "123"
    assert patient.name == "Alice Smith"
    assert patient.gender == "female"
    assert patient.birth_date == date(1990, 5, 20)

def test_parse_observation():
    obs_json = {
        "resourceType": "Observation",
        "status": "final",
        "code": {"coding": [{"code": "8867-4", "display": "Heart rate"}]},
        "effectiveDateTime": "2024-03-27T08:00:00Z",
        "valueQuantity": {"value": 75, "unit": "bpm"}
    }
    obs = FHIRParser.parse_observation(obs_json)
    assert obs is not None
    assert obs.display == "Heart rate"
    assert obs.value == 75.0
    assert obs.unit == "bpm"

def test_parse_bundle():
    bundle = {
        "resourceType": "Bundle",
        "entry": [
            {"resource": {"resourceType": "Patient", "id": "p1", "name": [{"family": "One"}]}},
            {
                "resource": {
                    "resourceType": "Observation",
                    "subject": {"reference": "Patient/p1"},
                    "code": {"text": "Scale"},
                    "valueQuantity": {"value": 70, "unit": "kg"},
                    "effectiveDateTime": "2024-01-01T00:00:00Z"
                }
            }
        ]
    }
    patients = FHIRParser.parse_bundle(bundle)
    assert len(patients) == 1
    assert patients[0].id == "p1"
    assert len(patients[0].observations) == 1
    assert patients[0].observations[0].display == "Scale"
