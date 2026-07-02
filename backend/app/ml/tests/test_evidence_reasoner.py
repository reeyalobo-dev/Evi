from app.ml.reasoning.evidence_reasoner import EvidenceReasoner


def test_reasoning_uses_evidence_blocks_without_boilerplate():
    candidate = {
        "candidate_id": "CAND_000001",
        "profile": {
            "current_title": "Senior AI Engineer",
            "years_of_experience": 6,
        },
    }
    evidence = {
        "skill_evidence": {
            "matched_fields": ["Python", "FAISS", "Semantic Search"],
            "missing_fields": ["AWS"],
            "score": 0.82,
        },
        "semantic_evidence": {"score": 0.81},
        "career_evidence": {"score": 0.62},
        "project_evidence": {"score": 0.71},
        "behavior_evidence": {"score": 0.31},
        "retrieval_evidence": {"bm25_score": 0.58},
    }
    behavior_trace = {
        "recruiter_response_rate": {"included": True, "value": 0.8},
    }

    result = EvidenceReasoner.generate_reasoning(
        candidate,
        evidence,
        {},
        {"behavior_score": 0.9, "project_score": 0.7, "career_score": 0.4},
        {},
        behavior_trace,
    )

    reasoning = result["reasoning"]

    assert "Track record" not in reasoning
    assert "Professional commitment" not in reasoning
    assert "Technical excellence" not in reasoning
    assert "Senior AI Engineer" in reasoning
    assert "Python" in reasoning
    assert "FAISS" in reasoning
    assert "Semantic Search" in reasoning
    assert len(reasoning.split()) >= 20
