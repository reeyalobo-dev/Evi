from typing import Dict, List


class ExplainabilityService:
    def explain(self, candidate: Dict[str, object], features: Dict[str, float], score: float) -> Dict[str, object]:
        strengths = []
        concerns = []
        if features.get("skill_overlap", 0) > 0.4:
            strengths.append("Strong skill alignment")
        if features.get("experience_match", 0) > 0.5:
            strengths.append("Experience level fits the role")
        if features.get("behavior_signal", 0) < 0.3:
            concerns.append("Behavioral readiness is below ideal")
        return {"candidate_id": candidate.get("candidate_id"), "score": score, "strengths": strengths, "concerns": concerns, "summary": "High technical relevance with explainable evidence."}
