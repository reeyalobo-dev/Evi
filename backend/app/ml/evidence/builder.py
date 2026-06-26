import re
from typing import Dict, List, Tuple


class EvidenceBuilder:
    def build(self, candidate: Dict[str, object], intent: Dict[str, object], job_description: str) -> Dict[str, object]:
        text = (job_description or "").lower()
        skills = [skill.get("name", "") for skill in candidate.get("skills", []) if isinstance(skill, dict)]
        skill_names = [s.lower() for s in skills]
        matched_skills = [skill for skill in intent.get("required_skills", []) if skill in text]
        overlap = len(set(skill_names) & set(intent.get("required_skills", [])))
        profile = candidate.get("profile", {})
        title_similarity = 1.0 if any(term in (profile.get("headline", "") or "").lower() for term in ["engineer", "developer", "ml", "data"]) else 0.5
        years = float(profile.get("years_of_experience", 0) or 0)
        evidence = {
            "semantic_evidence": {"score": min(1.0, 0.3 + 0.1 * overlap), "matched_fields": ["summary", "headline"], "missing_fields": [], "reason": "Profile aligns semantically with the job intent."},
            "skill_evidence": {"score": min(1.0, overlap / max(1, len(intent.get("required_skills", [])))), "matched_fields": matched_skills, "missing_fields": [skill for skill in intent.get("required_skills", []) if skill not in matched_skills], "reason": "Skill overlap indicates technical fit."},
            "career_evidence": {"score": min(1.0, max(0.0, years / max(1.0, float(intent.get("experience_years", 4))))), "matched_fields": [profile.get("current_title", "")], "missing_fields": [], "reason": "Experience level is compatible with the role."},
            "project_evidence": {"score": 0.8 if overlap > 0 else 0.2, "matched_fields": ["project experience"], "missing_fields": [], "reason": "Candidate has relevant project-oriented experience."},
            "behavior_evidence": {"score": min(1.0, float(profile.get("years_of_experience", 0) or 0) / 10.0), "matched_fields": ["behavior signals"], "missing_fields": [], "reason": "Behavioral context is supportive but not dominant."},
            "constraint_evidence": {"score": 0.8 if profile.get("country") else 0.5, "matched_fields": ["location"], "missing_fields": [], "reason": "Location and availability constraints are reasonable."},
        }
        return evidence
