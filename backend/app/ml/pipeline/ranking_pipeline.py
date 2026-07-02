import json
from pathlib import Path
from typing import Dict, List, Optional

from app.ml.embedding.service import EmbeddingService
from app.ml.evidence.builder import EvidenceBuilder
from app.ml.explainability.shap import ExplainabilityService
from app.ml.export.csv_exporter import CSVExporter
from app.ml.intent.extractor import IntentExtractor
from app.ml.reasoning.behavior_attribution import BehavioralAttributor
from app.ml.reasoning.evidence_reasoner import EvidenceReasoner
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
        candidate_records = []
        for _, _, candidate in retrieved:
            evidence = self.evidence_builder.build(candidate, intent, job_description)
            feature_vector = self._build_feature_vector(candidate, intent, evidence)
            candidate_records.append((candidate, evidence, feature_vector))
        if len(candidate_records) < 2:
            return []
        if not self.ranker.model_path.exists():
            training_rows = [record[2] for record in candidate_records[: min(20, len(candidate_records))]]
            self.ranker.train(training_rows, [0.8 + 0.01 * i for i in range(len(training_rows))])
        scores = self.ranker.predict([record[2] for record in candidate_records])
        behavior_attributor = BehavioralAttributor()
        ranked = []
        # load ranking weights from config
        import yaml
        from pathlib import Path
        cfg_path = Path(__file__).resolve().parents[3] / "config" / "ranking.yaml"
        weights = {"reranker": 0.6, "semantic": 0.1, "bm25": 0.05, "behavior": 0.1, "role_compatibility": 0.15}
        role_cfg = {"unrelated_title_penalty_threshold": 0.45, "unrelated_title_penalty_factor": 0.7}
        try:
            if cfg_path.exists():
                with cfg_path.open("r", encoding="utf-8") as fh:
                    cfg = yaml.safe_load(fh) or {}
                    weights.update(cfg.get("ranking_weights", {}))
                    role_cfg.update(cfg.get("role_compatibility", {}))
        except Exception:
            pass

        for (idx, bm25_score, candidate), (_, evidence, feature_vector), score in zip(retrieved, candidate_records, scores):
            # preserve internal precision; use reranker score as one input to fusion
            reranker_score = float(score)
            contributions = self._build_feature_contributions(feature_vector)
            total_contrib = sum(abs(v) for v in contributions.values()) or 1.0
            behavior_contribution = float(contributions.get("behavior_score", 0.0) or 0.0)
            behavior_norm = abs(behavior_contribution) / total_contrib

            semantic_score = float(evidence.get("semantic_evidence", {}).get("score", 0.0) or 0.0)
            bm25_s = float(bm25_score or 0.0)
            role_evidence = evidence.get("role_compatibility_evidence", {}) or {}
            role_score = float(role_evidence.get("score", 0.0) or 0.0)
            contributions["role_score"] = round(role_score * float(weights.get("role_compatibility", 0.0) or 0.0), 6)

            final_score = (
                weights.get("reranker", 0.0) * reranker_score
                + weights.get("semantic", 0.0) * semantic_score
                + weights.get("bm25", 0.0) * bm25_s
                + weights.get("behavior", 0.0) * behavior_norm
                + weights.get("role_compatibility", 0.0) * role_score
            )
            penalty_applied = False
            if bool(role_evidence.get("current_title_unrelated")) and role_score < float(role_cfg.get("unrelated_title_penalty_threshold", 0.45)):
                final_score *= float(role_cfg.get("unrelated_title_penalty_factor", 0.7))
                penalty_applied = True

            # attribution and reasoning
            behavior_trace = behavior_attributor.attribute(candidate, evidence, contributions, {"score": reranker_score})
            reasoning_data = EvidenceReasoner.generate_reasoning(candidate, evidence, intent, contributions, {"score": reranker_score, "role_score": role_score}, behavior_trace)

            ranked.append({
                "candidate_id": candidate.get("candidate_id"),
                # internal full-precision final score
                "score": float(final_score),
                "reranker_score": reranker_score,
                "semantic_score": semantic_score,
                "bm25_score": bm25_s,
                "role_score": round(role_score, 6),
                "behavior_contribution": round(behavior_norm, 6),
                "reasoning": reasoning_data.get("reasoning", ""),
                "explanation": reasoning_data,
                "feature_contributions": contributions,
                "behavior_trace": behavior_trace,
                "role_compatibility": role_evidence,
                "role_penalty_applied": penalty_applied,
                "ranking_audit": self._build_role_audit(candidate, role_score, semantic_score, final_score, role_evidence, penalty_applied),
            })
        # deterministic multi-criteria sorting with evidence-based tie-breakers
        def _sort_key(item):
            return (
                -item.get("score", 0.0),
                -item.get("reranker_score", 0.0),
                -item.get("semantic_score", 0.0),
                -item.get("role_score", 0.0),
                -item.get("bm25_score", 0.0),
                -item.get("feature_contributions", {}).get("skill_overlap", 0.0),
                -item.get("feature_contributions", {}).get("career_score", 0.0),
                -item.get("behavior_contribution", 0.0),
                str(item.get("candidate_id", "")),
            )

        ranked.sort(key=_sort_key)
        return ranked[:100]

    def _build_role_audit(
        self,
        candidate: Dict[str, object],
        role_score: float,
        semantic_score: float,
        final_score: float,
        role_evidence: Dict[str, object],
        penalty_applied: bool,
    ) -> Dict[str, object]:
        profile = candidate.get("profile", {}) or {}
        current_title = profile.get("current_title", "")
        if penalty_applied:
            audit_result = "WARNING"
            reason = "High semantic evidence but insufficient engineering role compatibility."
        elif bool(role_evidence.get("current_title_unrelated")):
            audit_result = "PASS"
            reason = "Career transition supported by technical evidence."
        else:
            audit_result = "PASS"
            reason = "Current or recent role evidence supports the target role."
        return {
            "candidate_id": candidate.get("candidate_id"),
            "current_title": current_title,
            "role_score": round(float(role_score), 6),
            "semantic_score": round(float(semantic_score), 6),
            "final_score": round(float(final_score), 6),
            "audit_result": audit_result,
            "reason": reason,
        }

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

    def _build_feature_contributions(self, feature_vector: list) -> Dict[str, float]:
        feature_names = [
            "skill_overlap",
            "experience_match",
            "semantic_score",
            "skill_score",
            "career_score",
            "project_score",
            "behavior_score",
            "constraint_score",
            "years_experience",
            "profile_completeness",
        ]
        import numpy as np

        if hasattr(self.ranker.model, "feature_importances_"):
            importances = np.array(self.ranker.model.feature_importances_, dtype=float)
            if len(importances) != len(feature_vector):
                importances = np.ones(len(feature_vector), dtype=float) / len(feature_vector)
        else:
            importances = np.ones(len(feature_vector), dtype=float) / len(feature_vector)

        contributions = {}
        for name, value, importance in zip(feature_names, feature_vector, importances):
            contributions[name] = round(float(abs(value) * importance), 6)
        return contributions

    def _build_feature_map(self, candidate: Dict[str, object], intent: Dict[str, object]) -> Dict[str, float]:
        profile = candidate.get("profile", {})
        skills = [skill.get("name", "") for skill in candidate.get("skills", []) if isinstance(skill, dict)]
        skill_overlap = len(set([s.lower() for s in skills]) & set(intent.get("required_skills", [])))
        experience_match = min(1.0, float(profile.get("years_of_experience", 0) or 0) / max(1.0, float(intent.get("experience_years", 4))))
        return {
            "skill_overlap": skill_overlap,
            "experience_match": experience_match,
            "behavior_signal": float(candidate.get("redrob_signals", {}).get("recruiter_response_rate", 0) or 0),
        }
