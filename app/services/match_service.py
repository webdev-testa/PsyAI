from typing import List, Dict, Any
from app.schemas import Psychologist

def match_psychologists(concerns: List[str], location: str | None, budget: str | None) -> List[Psychologist]:
    """
    Light adapter over your tools.psychologistMatcher.PsychologistMatcher.
    If not available, returns an empty list gracefully.
    """
    try:
        from tools.psychologistMatcher import PsychologistMatcher
    except Exception:
        return []

    try:
        matcher = PsychologistMatcher(data_path="psychologist_data.json")
        results: List[Dict[str, Any]] = matcher.match(concerns, location=location, budget=budget)
        return [Psychologist(
            name=r.get("name", "Unknown"),
            specialties=r.get("specialties", []),
            contact=r.get("contact"),
            location=r.get("location"),
        ) for r in results]
    except Exception:
        return []
