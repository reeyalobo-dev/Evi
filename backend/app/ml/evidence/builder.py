import re
from pathlib import Path
from typing import Dict, List, Tuple

import yaml


def _normalize_skill(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()


def _load_ranking_config() -> Dict[str, object]:
    config_path = Path(__file__).resolve().parents[3] / "config" / "ranking.yaml"
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _text_contains_any(text: str, terms: List[str]) -> List[str]:
    normalized = _normalize_skill(text)
    matches = []
    for term in terms:
        term_norm = _normalize_skill(term)
        if term_norm and re.search(rf"(^| ){re.escape(term_norm)}( |$)", normalized):
            matches.append(term)
    return matches


def _project_text(candidate: Dict[str, object]) -> Tuple[List[str], str]:
    project_titles = []
    project_parts = []
    for project in candidate.get("projects", []) or []:
        if not isinstance(project, dict):
            continue
        title = project.get("title") or project.get("name") or ""
        description = project.get("description") or ""
        if title:
            project_titles.append(str(title))
        project_parts.extend([str(title), str(description)])
    return project_titles, " ".join(project_parts)


class EvidenceBuilder:
    def __init__(self) -> None:
        self.ranking_config = _load_ranking_config()

    def build(self, candidate: Dict[str, object], intent: Dict[str, object], job_description: str) -> Dict[str, object]:
        profile = candidate.get("profile", {}) or {}
        candidate_skills = [skill.get("name", "") for skill in candidate.get("skills", []) if isinstance(skill, dict)]
        candidate_skill_names = [skill for skill in candidate_skills if skill]
        normalized_candidate_skills = [_normalize_skill(skill) for skill in candidate_skill_names]

        aliases = {
            "python": ["python", "py"],
            "backend": ["backend", "backend engineering", "backend systems", "api", "apis", "microservices"],
            "faiss": ["faiss"],
            "vector databases": ["vector database", "vector databases", "pgvector", "qdrant", "pinecone", "weaviate", "milvus", "vector search", "search index"],
            "retrieval": ["retrieval", "information retrieval", "semantic search", "search", "search systems"],
            "ranking": ["ranking", "ranker", "recommendation systems", "recommender systems", "ranking systems"],
            "production ml": ["production ml", "mlops", "model deployment", "production machine learning"],
            "machine learning": ["machine learning", "ml", "deep learning", "nlp", "computer vision", "transformers", "llms"],
        }

        matched_skills: List[str] = []
        for required_skill in intent.get("required_skills", []):
            required_norm = _normalize_skill(required_skill)
            for skill_name, normalized_skill_name in zip(candidate_skill_names, normalized_candidate_skills):
                if any(alias in normalized_skill_name for alias in aliases.get(required_skill, [required_norm])):
                    if skill_name not in matched_skills:
                        matched_skills.append(skill_name)
                        break

        overlap = len(matched_skills)
        years = float(profile.get("years_of_experience", 0) or 0)
        signals = candidate.get("redrob_signals", {}) or {}
        behavior_signals = {
            "recruiter_response_rate": float(signals.get("recruiter_response_rate", 0) or 0),
            "interview_completion_rate": float(signals.get("interview_completion_rate", 0) or 0),
            "profile_completeness_score": float(signals.get("profile_completeness_score", 0) or 0),
            "open_to_work_flag": signals.get("open_to_work_flag", False),
            "notice_period_days": int(signals.get("notice_period_days", 0) or 0),
            "github_activity_score": float(signals.get("github_activity_score", 0) or 0),
        }

        project_titles, project_text = _project_text(candidate)
        role_compatibility = self._build_role_compatibility(candidate, semantic_score=min(1.0, 0.3 + 0.1 * overlap), project_text=project_text)

        evidence = {
            "semantic_evidence": {"score": min(1.0, 0.3 + 0.1 * overlap), "matched_fields": [profile.get("headline", "")], "missing_fields": [], "reason": "Profile content aligns with the target role."},
            "skill_evidence": {"score": min(1.0, overlap / max(1, len(intent.get("required_skills", [])))), "matched_fields": matched_skills, "missing_fields": [skill for skill in intent.get("required_skills", []) if skill not in [s.lower() for s in matched_skills]], "reason": "Skill overlap indicates technical fit."},
            "career_evidence": {"score": min(1.0, max(0.0, years / max(1.0, float(intent.get("experience_years", 4))))), "matched_fields": [profile.get("current_title", "")], "missing_fields": [], "reason": "Experience level is compatible with the role."},
            "project_evidence": {"score": 0.8 if project_titles else 0.2, "matched_fields": project_titles[:3], "missing_fields": [], "reason": "Project experience is available for evidence-based discussion."},
            "behavior_evidence": {"score": min(1.0, float(profile.get("years_of_experience", 0) or 0) / 10.0), "matched_fields": ["behavior signals"], "missing_fields": [], "reason": "Behavioral context is supportive but not dominant.", "signals": behavior_signals},
            "constraint_evidence": {"score": 0.8 if profile.get("country") else 0.5, "matched_fields": ["location"], "missing_fields": [], "reason": "Location and availability constraints are reasonable."},
            "role_compatibility_evidence": role_compatibility,
        }
        return evidence

    def _build_role_compatibility(self, candidate: Dict[str, object], semantic_score: float, project_text: str) -> Dict[str, object]:
        cfg = self.ranking_config.get("role_compatibility", {}) if isinstance(self.ranking_config, dict) else {}
        weights = cfg.get("weights", {}) if isinstance(cfg, dict) else {}
        default_weights = {
            "title_similarity": 0.25,
            "career_evidence": 0.25,
            "technical_experience": 0.25,
            "project_evidence": 0.1,
            "semantic_similarity": 0.15,
        }
        default_weights.update({key: float(value) for key, value in weights.items() if key in default_weights})
        weight_total = sum(default_weights.values()) or 1.0

        relevant_titles = [str(term) for term in cfg.get("relevant_titles", [])] if isinstance(cfg, dict) else []
        unrelated_titles = [str(term) for term in cfg.get("unrelated_titles", [])] if isinstance(cfg, dict) else []
        domain_keywords = [str(term) for term in cfg.get("domain_keywords", [])] if isinstance(cfg, dict) else []

        profile = candidate.get("profile", {}) or {}
        current_title = str(profile.get("current_title", "") or "")
        headline = str(profile.get("headline", "") or "")
        summary = str(profile.get("summary", "") or "")
        career_history = [item for item in candidate.get("career_history", []) or [] if isinstance(item, dict)]
        recent_titles = " ".join(str(item.get("title", "") or "") for item in career_history[:3])
        career_text = " ".join(
            f"{item.get('title', '')} {item.get('description', '')}"
            for item in career_history
        )
        skills_text = " ".join(skill.get("name", "") for skill in candidate.get("skills", []) or [] if isinstance(skill, dict))

        title_text = f"{current_title} {headline} {recent_titles}"
        title_matches = _text_contains_any(title_text, relevant_titles)
        unrelated_matches = _text_contains_any(current_title, unrelated_titles)
        title_similarity = 1.0 if title_matches else 0.0
        if not title_matches and _text_contains_any(headline, domain_keywords):
            title_similarity = 0.35
        if unrelated_matches and not title_matches:
            title_similarity = min(title_similarity, 0.25)

        career_matches = _text_contains_any(career_text, domain_keywords + relevant_titles)
        career_evidence = min(1.0, len(set(career_matches)) / 4.0)

        technical_matches = _text_contains_any(f"{skills_text} {summary}", domain_keywords)
        technical_experience = min(1.0, len(set(technical_matches)) / 4.0)

        project_matches = _text_contains_any(project_text, domain_keywords)
        project_evidence = 1.0 if project_matches else (0.4 if project_text.strip() else 0.0)

        components = {
            "title_similarity": round(title_similarity, 4),
            "career_evidence": round(career_evidence, 4),
            "technical_experience": round(technical_experience, 4),
            "project_evidence": round(project_evidence, 4),
            "semantic_similarity": round(float(semantic_score), 4),
        }
        role_score = sum(components[key] * default_weights[key] for key in default_weights) / weight_total

        relevant_months = 0
        for item in career_history:
            item_text = f"{item.get('title', '')} {item.get('description', '')}"
            if _text_contains_any(item_text, relevant_titles + domain_keywords):
                relevant_months += int(item.get("duration_months", 0) or 0)

        return {
            "score": round(max(0.0, min(1.0, role_score)), 6),
            "components": components,
            "weights": {key: round(value, 4) for key, value in default_weights.items()},
            "matched_fields": {
                "title": title_matches,
                "career": sorted(set(career_matches))[:8],
                "technical": sorted(set(technical_matches))[:8],
                "project": sorted(set(project_matches))[:8],
            },
            "current_title_unrelated": bool(unrelated_matches and not title_matches),
            "unrelated_title_matches": unrelated_matches,
            "relevant_engineering_months": relevant_months,
            "reason": "Role compatibility combines title, career, technical, project, and semantic evidence.",
        }
