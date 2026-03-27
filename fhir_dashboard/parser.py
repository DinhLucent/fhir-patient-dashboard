"""
FHIR R4 Parser — Extracts display-ready data from complex FHIR JSON resources.
"""

import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from fhir_dashboard.models import Observation, Patient


class FHIRParser:
    """Parses FHIR JSON bundles/resources into domain models."""

    @staticmethod
    def parse_patient(data: Dict[str, Any]) -> Patient:
        """Parse a Patient resource."""
        patient_id = data.get("id", "unknown")
        
        # Name
        names = data.get("name", [])
        name_str = "Unknown"
        if names:
            name = names[0]
            family = name.get("family", "")
            given = " ".join(name.get("given", []))
            name_str = f"{given} {family}".strip()

        # Birth Date
        birth_str = data.get("birthDate", "1900-01-01")
        birth_date = date.fromisoformat(birth_str)

        # Contact
        telecoms = data.get("telecom", [])
        phone = ""
        for t in telecoms:
            if t.get("system") == "phone":
                phone = t.get("value", "")
                break

        return Patient(
            id=patient_id,
            name=name_str,
            gender=data.get("gender", "unknown"),
            birth_date=birth_date,
            telecom=phone,
        )

    @staticmethod
    def parse_observation(data: Dict[str, Any]) -> Optional[Observation]:
        """Parse an Observation resource (e.g., Heart Rate, BP)."""
        code_data = data.get("code", {})
        coding = code_data.get("coding", [{}])[0]
        display = coding.get("display") or code_data.get("text") or "Unknown"
        
        value_quantity = data.get("valueQuantity", {})
        value = value_quantity.get("value")
        if value is None:
            return None

        # Effective time
        time_str = data.get("effectiveDateTime")
        if not time_str:
            return None
            
        # Handle ISO strings (e.g., 2024-03-27T06:58:34Z)
        try:
            timestamp = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        except ValueError:
            timestamp = datetime.now()

        return Observation(
            code=coding.get("code", "unknown"),
            display=display,
            value=float(value),
            unit=value_quantity.get("unit", ""),
            timestamp=timestamp,
            status=data.get("status", "unknown"),
        )

    @classmethod
    def parse_bundle(cls, bundle_data: Dict[str, Any]) -> List[Patient]:
        """Parse a Bundle containing Patients and Observations."""
        patients_map: Dict[str, Patient] = {}
        observations: List[tuple[str, Observation]] = []

        entries = bundle_data.get("entry", [])
        for entry in entries:
            resource = entry.get("resource", {})
            res_type = resource.get("resourceType")

            if res_type == "Patient":
                p = cls.parse_patient(resource)
                patients_map[p.id] = p
            elif res_type == "Observation":
                obs = cls.parse_observation(resource)
                if obs:
                    subject_ref = resource.get("subject", {}).get("reference", "")
                    # ref format often "Patient/id"
                    patient_id = subject_ref.split("/")[-1]
                    observations.append((patient_id, obs))

        # Assign observations to patients
        for p_id, obs in observations:
            if p_id in patients_map:
                patients_map[p_id].observations.append(obs)

        return list(patients_map.values())
