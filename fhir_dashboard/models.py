"""
FHIR R4 Data Models — Lightweight Python representations for dashboard display.
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


@dataclass
class Observation:
    """Medical observation (e.g., vital signs, lab results)."""
    code: str
    display: str
    value: float
    unit: str
    timestamp: datetime
    status: str = "final"

    def __repr__(self) -> str:
        return f"Observation({self.display}={self.value}{self.unit})"


@dataclass
class Patient:
    """Patient demographic data."""
    id: str
    name: str
    gender: str
    birth_date: date
    telecom: str = ""
    address: str = ""
    observations: List[Observation] = field(default_factory=list)

    @property
    def age(self) -> int:
        today = date.today()
        return (
            today.year - self.birth_date.year - 
            ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )

    def __repr__(self) -> str:
        return f"Patient({self.name}, ID={self.id}, Obs={len(self.observations)})"
