import json
import random
from datetime import date, datetime, timedelta

def generate_patient(patient_id):
    given_names = ["John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Henry"]
    family_names = ["Smith", "Doe", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez"]
    
    gender = random.choice(["male", "female"])
    birth_date = date(random.randint(1950, 2010), random.randint(1, 12), random.randint(1, 28))
    
    return {
        "resourceType": "Patient",
        "id": f"p{patient_id}",
        "name": [
            {
                "family": random.choice(family_names),
                "given": [random.choice(given_names)]
            }
        ],
        "gender": gender,
        "birthDate": birth_date.isoformat(),
        "telecom": [
            {
                "system": "phone",
                "value": f"555-{random.randint(1000, 9999)}"
            }
        ]
    }

def generate_observation(patient_id, display, code, value_range, unit):
    # Generate 5 historical data points for each metric
    obs_list = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(5):
        timestamp = base_time + timedelta(hours=i*4)
        value = round(random.uniform(value_range[0], value_range[1]), 1)
        
        obs_list.append({
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": code,
                        "display": display
                    }
                ]
            },
            "subject": {
                "reference": f"Patient/p{patient_id}"
            },
            "effectiveDateTime": timestamp.isoformat().replace("+00:00", "Z"),
            "valueQuantity": {
                "value": value,
                "unit": unit
            }
        })
    return obs_list

def main():
    bundle = {
        "resourceType": "Bundle",
        "type": "collection",
        "entry": []
    }
    
    metrics = [
        ("Heart rate", "8867-4", (60, 100), "bpm"),
        ("Body temperature", "8310-5", (36.0, 38.5), "C"),
        ("Glucose", "2339-0", (80, 140), "mg/dL")
    ]
    
    for i in range(1, 13): # 12 patients
        patient = generate_patient(i)
        bundle["entry"].append({"resource": patient})
        
        for display, code, v_range, unit in metrics:
            obs_group = generate_observation(i, display, code, v_range, unit)
            for obs in obs_group:
                bundle["entry"].append({"resource": obs})
                
    with open("data/patient_bundle.json", "w") as f:
        json.dump(bundle, f, indent=4)
    print(f"Generated 12 patients and {12 * 3 * 5} observations.")

if __name__ == "__main__":
    main()
