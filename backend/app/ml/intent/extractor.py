import re
from typing import Dict, List


class IntentExtractor:
    def __init__(self) -> None:
        self.required_skills = ["python", "backend", "faiss", "vector databases", "retrieval", "ranking", "production ml", "machine learning"]
        self.preferred_skills = ["sql", "spark", "flask", "pytorch", "lightgbm", "search", "evaluation"]

    def extract(self, job_description: str) -> Dict[str, object]:
        text = (job_description or "").lower()
        required = [skill for skill in self.required_skills if skill in text]
        preferred = [skill for skill in self.preferred_skills if skill in text]
        if not preferred:
            preferred = ["sql", "spark", "flask"] if any(term in text for term in ["backend", "engineer", "python"]) else []
        years_match = re.search(r"(\d+(?:\.\d+)?)\s+years", text)
        experience_years = float(years_match.group(1)) if years_match else 4.0
        industries = ["ai", "ml", "software"] if any(term in text for term in ["ai", "ml", "software"]) else ["software"]
        negative_signals = []
        if "senior" in text:
            negative_signals.append("high seniority mismatch")
        return {
            "required_skills": required,
            "preferred_skills": preferred,
            "experience_years": experience_years,
            "industries": industries,
            "negative_signals": negative_signals,
            "hiring_philosophy": "technical relevance first, evidence-backed signal and recruiter readiness second",
        }
