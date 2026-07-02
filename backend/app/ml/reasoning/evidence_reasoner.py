import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


FORBIDDEN_PHRASES = [
    "building engineering work",
    "strong professional engagement",
    "solid technical foundation",
    "career trajectory",
    "professional engineering roles",
    "relevant production systems",
    "excellent candidate",
    "high technical relevance",
    "track record",
    "technical excellence",
    "production experience",
    "professional commitment",
    "technical impact",
    "hands-on capability",
    "capability",
    "career progression",
    "profile and career evidence mention",
    "headline positions",
    "visible evidence is thinner",
    "technical background aligns",
    "profile demonstrates",
    "current title aligns",
    "professional growth",
]

DOMAIN_PATTERNS: Sequence[Tuple[str, Sequence[str]]] = (
    ("Retrieval Systems", ("retrieval system", "retrieval systems", "information retrieval", "retrieval-focused", "retrieval focused")),
    ("Semantic Search", ("semantic search", "semantic retrieval")),
    ("Vector Databases", ("vector database", "vector databases", "faiss", "pgvector", "qdrant", "pinecone", "weaviate", "milvus")),
    ("Vector Search", ("vector search", "search index", "search indexes")),
    ("Ranking Systems", ("ranking system", "ranking systems", "ranker", "learning to rank", "ranking")),
    ("Recommendation Systems", ("recommendation system", "recommendation systems", "recommender system", "recommender systems", "recommendation")),
    ("Machine Learning", ("machine learning", "ml engineering", "ml workflows", "ml models", "modern ml", "deep learning")),
    ("LLMs", ("llm", "llms", "large language model", "large language models", "chatgpt", "gpt")),
    ("NLP", ("nlp", "natural language processing")),
    ("Fine Tuning", ("fine-tuning", "fine tuning", "finetuning", "lora")),
    ("Model Deployment", ("model deployment", "model serving", "deployed models", "deploying models", "bentoml")),
    ("Evaluation Frameworks", ("evaluation framework", "evaluation frameworks", "model evaluation", "evals")),
    ("ML Pipelines", ("ml pipeline", "ml pipelines", "feature pipeline", "feature pipelines")),
    ("Data Pipelines", ("data pipeline", "data pipelines", "streaming data pipelines")),
    ("Backend APIs", ("backend api", "backend apis", "fastapi", "rest api", "rest apis", "microservices")),
    ("Backend Systems", ("backend system", "backend systems", "backend/data", "backend engineering", "backend")),
    ("Distributed Systems", ("distributed system", "distributed systems")),
    ("Search Infrastructure", ("search infrastructure", "search platform", "search systems", "opensearch", "elasticsearch")),
    ("MLOps", ("mlops", "weights & biases", "wandb")),
    ("Cloud", ("aws", "azure", "gcp", "google cloud", "cloud")),
    ("Spark", ("spark", "pyspark", "spark streaming")),
    ("Kafka", ("kafka",)),
    ("Airflow", ("airflow", "apache airflow")),
    ("SQL", ("sql",)),
    ("Snowflake", ("snowflake",)),
)

RELEVANT_EDUCATION_TERMS = (
    "computer science",
    "artificial intelligence",
    "machine learning",
    "data science",
    "software engineering",
    "information technology",
)

RELEVANT_CERTIFICATION_TERMS = (
    "aws",
    "amazon web services",
    "azure",
    "gcp",
    "google cloud",
    "machine learning",
    "ml",
    "artificial intelligence",
    "ai",
    "data science",
    "kubernetes",
    "nlp",
    "deep learning",
)

STRONG_DOMAIN_SOURCES = {"candidate.skills", "candidate.certifications"}


def _normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _normalize_key(value: str) -> str:
    text = (value or "").lower()
    # Preserve technical hyphenated compounds
    protected_terms = {
        "ml-powered", "ai-driven", "cloud-native", "real-time",
        "event-driven", "vector-based", "state-of-the-art",
        "full-stack", "end-to-end", "fine-tuning", "retrieval-focused",
        "backend/data"
    }
    for term in protected_terms:
        if term in text:
            text = text.replace(term, term.replace("-", "\x00").replace("/", "\x01"))
    result = re.sub(r"[^a-z0-9\x00\x01]+", " ", text).strip()
    result = result.replace("\x00", "-").replace("\x01", "/")
    return result


def _word_count(text: str) -> int:
    return len(re.findall(r"\w+", text))


def _dedupe(values: Iterable[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for value in values:
        cleaned = _normalize_text(value)
        if not cleaned:
            continue
        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def _join_list(values: Sequence[str]) -> str:
    items = [value for value in values if value]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def _contains_phrase(text: str, phrase: str) -> bool:
    normalized_text = _normalize_key(text)
    normalized_phrase = _normalize_key(phrase)
    if not normalized_phrase:
        return False
    return bool(re.search(rf"(^| ){re.escape(normalized_phrase)}( |$)", normalized_text))


def _supports_value(text: str, value: str) -> bool:
    """Check if text supports/contains the value using token-based matching."""
    if _contains_phrase(text, value):
        return True
    
    # Token-based matching for formatted education strings like "M.Sc in Data Science"
    text_lower = text.lower()
    value_lower = value.lower()
    
    # For education matches, also check if tokens appear (even with variations)
    text_tokens = set(_normalize_key(text).split())
    value_tokens = [token for token in _normalize_key(value).split() if token not in {"in", "of", "and"}]
    
    if value_tokens and all(token in text_tokens for token in value_tokens):
        return True
    
    # Check for specific education patterns (e.g., "M.Sc in Data Science" against "M.Sc Data Science")
    value_parts = re.split(r'\s+', value_lower)
    for i in range(len(value_parts)):
        part = value_parts[i]
        if part and len(part) > 2 and part in text_lower:
            # Check if multiple key parts are present
            key_parts = [p for p in value_parts if len(p) > 3 and p not in {"data", "science", "computer", "engineering"}]
            if all(p in text_lower for p in key_parts):
                return True
    
    return False


def _field_text(candidate: Dict[str, object], source: str) -> str:
    profile = candidate.get("profile", {}) or {}
    if source == "candidate.skills":
        return " ".join(skill.get("name", "") for skill in candidate.get("skills", []) or [] if isinstance(skill, dict))
    if source == "career_history":
        return " ".join(
            f"{item.get('title', '')} {item.get('description', '')}"
            for item in candidate.get("career_history", []) or []
            if isinstance(item, dict)
        )
    if source == "candidate.profile":
        return f"{profile.get('headline', '')} {profile.get('summary', '')}"
    if source == "candidate.certifications":
        return " ".join(
            f"{item.get('name', '')} {item.get('issuer', '')}"
            for item in candidate.get("certifications", []) or []
            if isinstance(item, dict)
        )
    if source == "candidate.education":
        return " ".join(
            f"{item.get('degree', '')} {item.get('field_of_study', '')}"
            for item in candidate.get("education", []) or []
            if isinstance(item, dict)
        )
    if source == "candidate.projects":
        return " ".join(
            f"{item.get('title', item.get('name', ''))} {item.get('description', '')}"
            for item in candidate.get("projects", []) or []
            if isinstance(item, dict)
        )
    return ""


def _format_years(value: Any) -> Optional[str]:
    if value in (None, ""):
        return None
    try:
        years = float(value)
    except (TypeError, ValueError):
        return None
    whole_years = int(years)
    fraction = years - whole_years
    if years < 1:
        return "less than one year"
    if fraction >= 0.75:
        return f"nearly {whole_years + 1} years"
    if fraction >= 0.25:
        return f"over {whole_years} years"
    return f"{whole_years} years"


def _candidate_skill_names(candidate: Dict[str, object]) -> List[str]:
    return [
        _normalize_text(skill.get("name", ""))
        for skill in candidate.get("skills", []) or []
        if isinstance(skill, dict) and _normalize_text(skill.get("name", ""))
    ]


def _matched_skills(candidate: Dict[str, object], evidence: Dict[str, object]) -> List[str]:
    raw_matches = [s for s in evidence.get("skill_evidence", {}).get("matched_fields", []) if s]
    candidate_skills = _candidate_skill_names(candidate)
    if not candidate_skills:
        return _dedupe(raw_matches)
    skill_lookup = {_normalize_key(skill): skill for skill in candidate_skills}
    result = []
    for skill in raw_matches:
        key = _normalize_key(str(skill))
        if key in skill_lookup:
            result.append(skill_lookup[key])
    return _dedupe(result)


def _domain_sources(candidate: Dict[str, object]) -> Dict[str, Dict[str, List[str]]]:
    source_texts = {
        "candidate.skills": _field_text(candidate, "candidate.skills"),
        "career_history": _field_text(candidate, "career_history"),
        "candidate.projects": _field_text(candidate, "candidate.projects"),
        "candidate.profile": _field_text(candidate, "candidate.profile"),
        "candidate.certifications": _field_text(candidate, "candidate.certifications"),
        "candidate.education": _field_text(candidate, "candidate.education"),
    }
    domains: Dict[str, Dict[str, List[str]]] = {}
    for label, aliases in DOMAIN_PATTERNS:
        for source, text in source_texts.items():
            matched_aliases = [alias for alias in aliases if _contains_phrase(text, alias)]
            if matched_aliases:
                item = domains.setdefault(label, {"sources": [], "evidence": []})
                item["sources"].append(source)
                item["evidence"].extend(matched_aliases)

    supported: Dict[str, Dict[str, List[str]]] = {}
    for label, item in domains.items():
        sources = _dedupe(item.get("sources", []))
        has_strong_source = bool(STRONG_DOMAIN_SOURCES & set(sources))
        if has_strong_source or len(sources) >= 2:
            supported[label] = {
                "sources": sources,
                "evidence": _dedupe(item.get("evidence", [])),
            }
    return supported


def extract_profile_evidence(candidate: Dict[str, object]) -> Dict[str, object]:
    profile = candidate.get("profile", {}) or {}
    role = _normalize_text(profile.get("current_title")) or _normalize_text(profile.get("headline")) or "Professional"
    return {
        "role": role,
        "years_text": _format_years(profile.get("years_of_experience")),
        "headline": _normalize_text(profile.get("headline")),
        "summary": _normalize_text(profile.get("summary")),
        "current_company": _normalize_text(profile.get("current_company")),
        "current_industry": _normalize_text(profile.get("current_industry")),
    }


def extract_career_evidence(candidate: Dict[str, object]) -> Dict[str, object]:
    titles = []
    descriptions = []
    for item in candidate.get("career_history", []) or []:
        if isinstance(item, dict):
            titles.append(_normalize_text(item.get("title")))
            descriptions.append(_normalize_text(item.get("description")))
    return {
        "titles": _dedupe(titles),
        "descriptions": [description for description in descriptions if description],
        "domains": _domain_sources(candidate),
    }


def extract_domain_evidence(candidate: Dict[str, object], matched_skills: Optional[Sequence[str]] = None) -> Dict[str, object]:
    return {
        "matched_skills": _dedupe(matched_skills or []),
        "domains": _domain_sources(candidate),
    }


def extract_certification_evidence(candidate: Dict[str, object], job_intent: Optional[Dict[str, object]] = None) -> Dict[str, List[str]]:
    certifications = []
    for cert in candidate.get("certifications", []) or []:
        if not isinstance(cert, dict):
            continue
        name = _normalize_text(cert.get("name"))
        issuer = _normalize_text(cert.get("issuer"))
        combined = f"{name} {issuer}".lower()
        if name and any(term in combined for term in RELEVANT_CERTIFICATION_TERMS):
            certifications.append(name)

    education = []
    for item in candidate.get("education", []) or []:
        if not isinstance(item, dict):
            continue
        field = _normalize_text(item.get("field_of_study"))
        degree = _normalize_text(item.get("degree"))
        combined = f"{degree} {field}".lower()
        if field and any(term in combined for term in RELEVANT_EDUCATION_TERMS):
            # Format education strings to support various formats
            if degree:
                # Handle various degree formats: M.Sc, B.Tech, Master's, Bachelor's, etc.
                education.append(f"{degree} in {field}")
            else:
                education.append(field)

    return {"certifications": _dedupe(certifications), "education": _dedupe(education)}


def extract_behavioral_evidence(behavior_trace: Dict[str, object]) -> List[Dict[str, object]]:
    labels: List[Dict[str, object]] = []
    for signal_name, signal_data in (behavior_trace or {}).items():
        if not isinstance(signal_data, dict) or not bool(signal_data.get("included")):
            continue
        value = signal_data.get("value")
        label = ""
        if signal_name == "recruiter_response_rate" and isinstance(value, (int, float)) and value >= 0.65:
            label = "high recruiter responsiveness"
        elif signal_name == "interview_completion_rate" and isinstance(value, (int, float)) and value >= 0.7:
            label = "high interview completion"
        elif signal_name == "profile_completeness_score" and isinstance(value, (int, float)) and value >= 70:
            label = "complete profile"
        elif signal_name == "open_to_work_flag" and value is True:
            label = "open to work"
        elif signal_name == "notice_period_days" and isinstance(value, (int, float)) and value <= 30:
            label = "short notice period"
        elif signal_name == "github_activity_score" and isinstance(value, (int, float)) and value >= 20:
            label = "recent GitHub activity"
        if label:
            labels.append({"label": label, "signal": signal_name, "value": value})
    seen = set()
    result = []
    for item in labels:
        if item["label"] not in seen:
            seen.add(item["label"])
            result.append(item)
    return result


def _sentence_trace(sentence: str, sources: Sequence[str], evidence: Sequence[str], feature: str, contribution: Any) -> Dict[str, object]:
    return {
        "sentence": sentence,
        "source": _dedupe(sources),
        "evidence": _dedupe(str(item) for item in evidence if item),
        "feature_contribution": {feature: contribution},
    }


def _append_sentence(
    sentences: List[str],
    trace: List[Dict[str, object]],
    sentence: str,
    sources: Sequence[str],
    evidence: Sequence[str],
    feature: str,
    contribution: Any,
    max_words: int = 70,
) -> None:
    clean = _normalize_text(sentence)
    if not clean:
        return
    if not clean.endswith("."):
        clean += "."
    if _word_count(" ".join(sentences + [clean])) <= max_words:
        sentences.append(clean)
        trace.append(_sentence_trace(clean, sources, evidence, feature, contribution))


def _headline_focus(headline: str, role: str) -> str:
    if not headline or headline.lower() == role.lower():
        return ""
    parts = [part.strip() for part in headline.split("|") if part.strip()]
    for part in reversed(parts):
        if part.lower() != role.lower():
            return part
    return headline


def _summary_focus(summary: str) -> str:
    if not summary:
        return ""
    sentences = [part.strip() for part in re.split(r"(?<=[.!?])\s+", summary) if part.strip()]
    for sentence in sentences:
        if any(_contains_phrase(sentence, alias) for _, aliases in DOMAIN_PATTERNS for alias in aliases):
            return sentence.rstrip(".")
    return sentences[0].rstrip(".") if sentences else ""


def compose_reasoning(
    profile_evidence: Dict[str, object],
    domain_evidence: Dict[str, object],
    career_evidence: Dict[str, object],
    certification_evidence: Dict[str, List[str]],
    behavioral_evidence: Sequence[Dict[str, object]],
    feature_contributions: Optional[Dict[str, float]] = None,
) -> Tuple[str, List[Dict[str, object]]]:
    feature_contributions = feature_contributions or {}
    role = str(profile_evidence.get("role") or "Professional")
    years_text = profile_evidence.get("years_text")
    headline = str(profile_evidence.get("headline") or "")
    sentences: List[str] = []
    trace: List[Dict[str, object]] = []

    role_sentence = f"Currently working as {role}"
    if years_text:
        role_sentence += f" with {years_text} of experience"
    _append_sentence(
        sentences,
        trace,
        role_sentence,
        ["candidate.profile.current_title", "candidate.profile.years_of_experience"],
        [role, str(years_text or "")],
        "role_score",
        feature_contributions.get("role_score"),
    )

    matched_skills = domain_evidence.get("matched_skills", [])[:4]
    if matched_skills:
        _append_sentence(
            sentences,
            trace,
            f"Experience includes {_join_list(matched_skills)} from the candidate's skills profile",
            ["candidate.skills"],
            matched_skills,
            "skill_score",
            feature_contributions.get("skill_score"),
        )

    domains: Dict[str, Dict[str, List[str]]] = domain_evidence.get("domains", {}) or {}
    prioritized_domains = list(domains.keys())[:4]
    if prioritized_domains:
        domain_sources = []
        domain_evidence_values = []
        for domain in prioritized_domains:
            domain_sources.extend(domains[domain].get("sources", []))
            domain_evidence_values.extend(domains[domain].get("evidence", []))
        source_set = set(domain_sources)
        if "career_history" in source_set:
            prefix = "Career history highlights"
        elif "candidate.skills" in source_set:
            prefix = "Technical experience spans"
        else:
            prefix = "Background includes"
        _append_sentence(
            sentences,
            trace,
            f"{prefix} {_join_list(prioritized_domains)}",
            domain_sources,
            domain_evidence_values + prioritized_domains,
            "career_score",
            feature_contributions.get("career_score"),
        )

    certifications = certification_evidence.get("certifications", [])[:2]
    education = certification_evidence.get("education", [])[:1]
    if certifications:
        _append_sentence(
            sentences,
            trace,
            f"{_join_list(certifications)} adds directly relevant certification evidence",
            ["candidate.certifications"],
            certifications,
            "semantic_score",
            feature_contributions.get("semantic_score"),
        )
    elif education:
        _append_sentence(
            sentences,
            trace,
            f"Education includes {_join_list(education)}",
            ["candidate.education"],
            education,
            "semantic_score",
            feature_contributions.get("semantic_score"),
        )

    if behavioral_evidence:
        labels = [item["label"] for item in behavioral_evidence[:2]]
        signals = [item["signal"] for item in behavioral_evidence[:2]]
        _append_sentence(
            sentences,
            trace,
            f"Hiring readiness is supported by {_join_list(labels)}",
            ["behavior_trace"],
            signals + labels,
            "behavior_score",
            feature_contributions.get("behavior_score"),
        )

    current_word_count = _word_count(" ".join(sentences))
    if current_word_count < 45:
        # Try to add one supplementary sentence to reach 45-70 word range
        added = False
        
        # Try headline focus first
        focus = _headline_focus(headline, role)
        if focus and not added:
            _append_sentence(
                sentences,
                trace,
                f"Recent focus includes {focus}",
                ["candidate.profile.headline"],
                [headline],
                "semantic_score",
                feature_contributions.get("semantic_score"),
            )
            current_word_count = _word_count(" ".join(sentences))
            added = current_word_count >= 45
        
        # Try industry if still under 45
        if current_word_count < 45 and not added:
            industry = str(profile_evidence.get("current_industry") or "")
            if industry:
                _append_sentence(
                    sentences,
                    trace,
                    f"Industry experience includes {industry}",
                    ["candidate.profile.current_industry"],
                    [industry],
                    "career_score",
                    feature_contributions.get("career_score"),
                )
                current_word_count = _word_count(" ".join(sentences))
                added = current_word_count >= 45
        
        # Try summary focus if still under 45
        if current_word_count < 45 and not added:
            summary_focus = _summary_focus(str(profile_evidence.get("summary") or ""))
            if summary_focus:
                _append_sentence(
                    sentences,
                    trace,
                    f"Summary notes {summary_focus}",
                    ["candidate.profile.summary"],
                    [summary_focus],
                    "semantic_score",
                    feature_contributions.get("semantic_score"),
                )

    reasoning = re.sub(r"\s+", " ", " ".join(sentences)).strip()
    if not reasoning.endswith("."):
        reasoning += "."
    return reasoning, trace


def _matched_skills_from_validation_payload(evidence: Dict[str, object]) -> List[str]:
    if not isinstance(evidence, dict):
        return []
    skill_evidence = evidence.get("skill_evidence", {})
    if isinstance(skill_evidence, dict):
        return [s for s in skill_evidence.get("matched_fields", []) if s]
    parsed: List[str] = []
    for strength in evidence.get("strengths", []) or []:
        if isinstance(strength, str) and strength.lower().startswith("matched skills:"):
            parsed.extend(skill.strip() for skill in strength.split(":", 1)[1].split(",") if skill.strip())
    return _dedupe(parsed)


def _trace_from_payload(evidence: Dict[str, object]) -> List[Dict[str, object]]:
    if isinstance(evidence, dict):
        trace = evidence.get("evidence_trace", [])
        if isinstance(trace, list):
            return [item for item in trace if isinstance(item, dict)]
    return []


class EvidenceReasoner:
    @classmethod
    def build_profile(
        cls,
        candidate: Dict[str, object],
        evidence: Dict[str, object],
        behavior_trace: Dict[str, object],
    ) -> Dict[str, object]:
        profile_evidence = extract_profile_evidence(candidate)
        matched_skills = _matched_skills(candidate, evidence)
        domains = extract_domain_evidence(candidate, matched_skills)
        scores = {
            "semantic": float(evidence.get("semantic_evidence", {}).get("score", 0) or 0),
            "skill": float(evidence.get("skill_evidence", {}).get("score", 0) or 0),
            "career": float(evidence.get("career_evidence", {}).get("score", 0) or 0),
            "project": float(evidence.get("project_evidence", {}).get("score", 0) or 0),
            "behavior": float(evidence.get("behavior_evidence", {}).get("score", 0) or 0),
            "role": float(evidence.get("role_compatibility_evidence", {}).get("score", 0) or 0),
        }
        return {
            "current_title": profile_evidence.get("role"),
            "years_of_experience": profile_evidence.get("years_text"),
            "top_skills": matched_skills[:4],
            "domains": list((domains.get("domains", {}) or {}).keys())[:4],
            "behavioral_signals": extract_behavioral_evidence(behavior_trace),
            "score_decomposition": scores,
        }

    @classmethod
    def extract_best_evidence(cls, profile: Dict[str, object]) -> Dict[str, List[str]]:
        result: Dict[str, List[str]] = {}
        if profile.get("top_skills"):
            result["skills"] = profile["top_skills"][:4]
        if profile.get("domains"):
            result["domains"] = profile["domains"][:4]
        if profile.get("behavioral_signals"):
            result["behavior"] = [item["label"] for item in profile["behavioral_signals"][:2]]
        return result

    @classmethod
    def compose(cls, blocks: List[Optional[str]]) -> str:
        parts = [block for block in blocks if block]
        reasoning = re.sub(r"\s+", " ", " ".join(parts)).strip() or "Candidate profile available."
        return reasoning if reasoning.endswith(".") else f"{reasoning}."

    @classmethod
    def generate_reasoning(
        cls,
        candidate: Dict[str, object],
        evidence: Dict[str, object],
        job_intent: Dict[str, object],
        feature_contributions: Dict[str, float],
        ranking_metadata: Dict[str, object],
        behavior_trace: Dict[str, object],
    ) -> Dict[str, object]:
        matched_skills = _matched_skills(candidate, evidence)
        profile_evidence = extract_profile_evidence(candidate)
        career_evidence = extract_career_evidence(candidate)
        domain_evidence = extract_domain_evidence(candidate, matched_skills)
        certification_evidence = extract_certification_evidence(candidate, job_intent)
        behavioral_evidence = extract_behavioral_evidence(behavior_trace)
        reasoning, evidence_trace = compose_reasoning(
            profile_evidence,
            domain_evidence,
            career_evidence,
            certification_evidence,
            behavioral_evidence,
            feature_contributions,
        )
        validation_profile = cls.build_profile(candidate, evidence, behavior_trace)
        validation = cls.validate_reasoning(candidate, {**evidence, "evidence_trace": evidence_trace}, reasoning, validation_profile, behavior_trace)

        strengths = []
        if matched_skills:
            strengths.append(f"Matched skills: {', '.join(matched_skills[:4])}")
        domains = list((domain_evidence.get("domains", {}) or {}).keys())
        if domains:
            strengths.append(f"Evidence domains: {', '.join(domains[:4])}")

        return {
            "reasoning": reasoning,
            "strengths": strengths,
            "concerns": [],
            "profile": {
                "current_title": profile_evidence.get("role"),
                "years_of_experience": profile_evidence.get("years_text"),
            },
            "evidence_trace": evidence_trace,
            "validation": validation,
        }

    @classmethod
    def validate_reasoning(
        cls,
        candidate: Dict[str, object],
        evidence: Dict[str, object],
        reasoning: str,
        profile: Dict[str, object],
        behavior_trace: Dict[str, object],
    ) -> Dict[str, Any]:
        normalized_reasoning = reasoning.lower()
        profile_data = candidate.get("profile", {}) or {}
        role = _normalize_text(profile_data.get("current_title", "")) or _normalize_text(profile_data.get("headline", "")) or ""
        candidate_skill_keys = {_normalize_key(skill) for skill in _candidate_skill_names(candidate)}
        matched_skills = _matched_skills_from_validation_payload(evidence)
        trace = _trace_from_payload(evidence)

        role_validation_failures = []
        if role and role.lower() not in normalized_reasoning:
            role_validation_failures.append(role)

        skill_validation_failures = []
        if candidate_skill_keys:
            for skill in matched_skills:
                if _normalize_key(skill) not in candidate_skill_keys:
                    skill_validation_failures.append(skill)
                elif skill.lower() not in normalized_reasoning and len(matched_skills) <= 4:
                    skill_validation_failures.append(skill)

        placeholder_phrases = [phrase for phrase in FORBIDDEN_PHRASES if phrase.lower() in normalized_reasoning]
        unsupported_claims = list(placeholder_phrases)

        behavior_terms = [
            "recruiter responsiveness",
            "interview completion",
            "open to work",
            "short notice period",
            "recent github activity",
            "complete profile",
        ]
        behavior_used = bool(any(item.get("included") for item in (behavior_trace or {}).values() if isinstance(item, dict)))
        behavior_misattributions = []
        if any(term in normalized_reasoning for term in behavior_terms) and not behavior_used:
            behavior_misattributions.append("Behavioral statement used without contributing evidence")

        sentences = [sentence.strip() + "." for sentence in re.split(r"\.\s+", reasoning.strip().rstrip(".")) if sentence.strip()]
        traced_sentences = {str(item.get("sentence", "")).strip() for item in trace}
        missing_evidence = [sentence for sentence in sentences if sentence not in traced_sentences]

        # Source-aware validation: validate claims only against their declared sources
        certification_text = _field_text(candidate, "candidate.certifications")
        education_text = _field_text(candidate, "candidate.education")
        career_text = _field_text(candidate, "career_history")
        skills_text = _field_text(candidate, "candidate.skills")
        behavior_signals = (behavior_trace or {})

        for item in trace:
            sources = set(item.get("source", []) or [])
            for value in item.get("evidence", []) or []:
                value_text = str(value)
                if not value_text:
                    continue
                
                # Validate based on source type
                if sources == {"candidate.certifications"}:
                    if not _supports_value(certification_text, value_text):
                        missing_evidence.append(value_text)
                elif sources == {"candidate.education"}:
                    if not _supports_value(education_text, value_text):
                        missing_evidence.append(value_text)
                elif sources == {"career_history"}:
                    if not _supports_value(career_text, value_text):
                        missing_evidence.append(value_text)
                elif sources == {"candidate.skills"}:
                    if not _supports_value(skills_text, value_text):
                        missing_evidence.append(value_text)
                elif "behavior_trace" in sources:
                    # For behavioral evidence, check if the signal is included
                    pass  # Behavior is handled separately via behavior_misattributions
                # For mixed sources, don't fail - allow mixed-source reasoning

        validation_status = "PASS"
        if unsupported_claims or placeholder_phrases or skill_validation_failures or role_validation_failures or behavior_misattributions or missing_evidence:
            validation_status = "FAIL"

        return {
            "unsupported_claims": unsupported_claims,
            "missing_evidence": _dedupe(missing_evidence),
            "placeholder_phrases": placeholder_phrases,
            "duplicate_reasonings": [],
            "behavior_misattributions": behavior_misattributions,
            "skill_validation_failures": _dedupe(skill_validation_failures),
            "role_validation_failures": role_validation_failures,
            "project_validation_failures": [],
            "validation_status": validation_status,
        }
