import json
from pathlib import Path
from typing import Dict, List, Optional

from app.ml.embedding.service import EmbeddingService
from app.ml.evidence.builder import EvidenceBuilder
from app.ml.explainability.shap import ExplainabilityService
from app.ml.export.csv_exporter import CSVExporter
from app.ml.intent.extractor import IntentExtractor
from app.ml.ranking.model import LambdaMartRanker
from app.ml.retrieval.hybrid import HybridRetriever


class RankingPipeline:
    def __init__(self, data_path: Optional[str] = None) -> None:
        candidate_path = Path(data_path) if data_path else None
        if candidate_path is None:
            possible_paths = [
                Path(__file__).resolve().parents[2] / "India_runs_data_and_ai_challenge" / "candidates.jsonl",
                Path(__file__).resolve().parents[2] / "backend" / "India_runs_data_and_ai_challenge" / "candidates.jsonl",
                Path.cwd() / "India_runs_data_and_ai_challenge" / "candidates.jsonl",
            ]
            for path in possible_paths:
                if path.exists():
                    candidate_path = path
                    break
        if candidate_path is None:
            raise FileNotFoundError("Could not find candidates.jsonl in the expected backend data folders")
        self.data_path = candidate_path
        self.intent_extractor = IntentExtractor()
        self.embedding_service = EmbeddingService()
        self.evidence_builder = EvidenceBuilder()
        self.explainability_service = ExplainabilityService()
        self.exporter = CSVExporter()
        self.ranker = LambdaMartRanker()
        self._candidates = None
        self._retriever = None

    @property
    def candidates(self) -> List[Dict[str, object]]:
        if self._candidates is None:
            self._candidates = [json.loads(line) for line in self.data_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        return self._candidates

    def run(self, job_description: str) -> List[Dict[str, object]]:
        intent = self.intent_extractor.extract(job_description)
        self._retriever = HybridRetriever(self.candidates[:5000])
        retrieved = self._retriever.retrieve(job_description, top_k=200)
        if not retrieved:
            return []
        features = []
        for _, _, candidate in retrieved:
            evidence = self.evidence_builder.build(candidate, intent, job_description)
            feature_vector = self._build_feature_vector(candidate, intent, evidence)
            features.append(feature_vector)
        if len(features) < 2:
            return []
        if not self.ranker.model_path.exists():
            training_rows = features[: min(20, len(features))]
            self.ranker.train(features[: min(20, len(features))], [0.8 + 0.01 * i for i in range(len(training_rows))])
        scores = self.ranker.predict(features)
        ranked = []
        for (idx, bm25_score, candidate), score in zip(retrieved, scores):
            explanation = self.explainability_service.explain(candidate, self._build_feature_map(candidate, intent), float(score))
            ranked.append({
                "candidate_id": candidate.get("candidate_id"),
                "score": float(score),
                "reasoning": explanation["summary"],
                "explanation": explanation,
            })
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[:100]

    def _build_feature_vector(self, candidate: Dict[str, object], intent: Dict[str, object], evidence: Dict[str, object]) -> list:
        profile = candidate.get("profile", {})
        skills = [skill.get("name", "") for skill in candidate.get("skills", []) if isinstance(skill, dict)]
        skill_overlap = len(set([s.lower() for s in skills]) & set(intent.get("required_skills", [])))
        experience_match = min(1.0, float(profile.get("years_of_experience", 0) or 0) / max(1.0, float(intent.get("experience_years", 4))))
        return [
            float(skill_overlap),
            float(experience_match),
            float(evidence["semantic_evidence"]["score"]),
            float(evidence["skill_evidence"]["score"]),
            float(evidence["career_evidence"]["score"]),
            float(evidence["project_evidence"]["score"]),
            float(evidence["behavior_evidence"]["score"]),
            float(evidence["constraint_evidence"]["score"]),
            float(profile.get("years_of_experience", 0) or 0),
            float(profile.get("profile_completeness_score", 0) or 0),
        ]

    def _build_feature_map(self, candidate: Dict[str, object], intent: Dict[str, object]) -> Dict[str, float]:
        profile = candidate.get("profile", {})
        skills = [skill.get("name", "") for skill in candidate.get("skills", []) if isinstance(skill, dict)]
        skill_overlap = len(set([s.lower() for s in skills]) & set(intent.get("required_skills", [])))
        experience_match = min(1.0, float(profile.get("years_of_experience", 0) or 0) / max(1.0, float(intent.get("experience_years", 4))))
        return {
            "skill_overlap": skill_overlap,
            "experience_match": experience_match,
            "behavior_signal": float(profile.get("recruiter_response_rate", 0) or 0),
        }
