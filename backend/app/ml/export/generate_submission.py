import json
from pathlib import Path
from typing import List, Dict

from app.ml.pipeline.ranking_pipeline import RankingPipeline
from app.ml.reasoning.evidence_reasoner import EvidenceReasoner


def _normalize_results(results: List[Dict[str, object]]) -> List[Dict[str, object]]:
    normalized = []
    for result in results[:100]:
        score = float(result.get("score", 0.0))
        score = float(f"{score:.6f}")
        normalized.append({
            "candidate_id": result.get("candidate_id"),
            "score": score,
            "reasoning": result.get("reasoning", ""),
        })
    normalized.sort(key=lambda item: (-item["score"], str(item.get("candidate_id", ""))))
    return normalized


def generate(job_description: str, output_path: str = 'results/submission.csv'):
    pipeline = RankingPipeline()
    results = pipeline.run(job_description)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    candidate_lookup = {candidate.get("candidate_id"): candidate for candidate in pipeline.candidates if candidate.get("candidate_id")}
    validations = []
    evidence_trace = []
    for result in results:
        candidate = candidate_lookup.get(result.get("candidate_id"))
        if candidate is None:
            continue
        validation = EvidenceReasoner.validate_reasoning(
            candidate,
            result.get("explanation", {}),
            result.get("reasoning", ""),
            candidate.get("profile", {}),
            result.get("behavior_trace", {}),
        )
        validations.append(validation)
        evidence_trace.append({
            "candidate_id": result.get("candidate_id"),
            "reasoning": result.get("reasoning", ""),
            "sentences": result.get("explanation", {}).get("evidence_trace", []),
        })

    duplicate_reasonings = []
    seen_reasonings = {}
    for result in results:
        reasoning = result.get("reasoning", "")
        if reasoning in seen_reasonings:
            duplicate_reasonings.append({
                "candidate_id": result.get("candidate_id"),
                "duplicate_of": seen_reasonings[reasoning],
            })
        else:
            seen_reasonings[reasoning] = result.get("candidate_id")

    report = {
        "total_candidates": len(results),
        "unsupported_claims": [item for validation in validations for item in validation.get("unsupported_claims", [])],
        "missing_evidence": [item for validation in validations for item in validation.get("missing_evidence", [])],
        "placeholder_phrases": [item for validation in validations for item in validation.get("placeholder_phrases", [])],
        "duplicate_reasonings": duplicate_reasonings,
        "behavior_misattributions": [item for validation in validations for item in validation.get("behavior_misattributions", [])],
        "skill_validation_failures": [item for validation in validations for item in validation.get("skill_validation_failures", [])],
        "role_validation_failures": [item for validation in validations for item in validation.get("role_validation_failures", [])],
        "project_validation_failures": [item for validation in validations for item in validation.get("project_validation_failures", [])],
    }
    report["validation_status"] = "PASS" if not any(
        report[key]
        for key in [
            "unsupported_claims",
            "missing_evidence",
            "placeholder_phrases",
            "duplicate_reasonings",
            "behavior_misattributions",
            "skill_validation_failures",
            "role_validation_failures",
            "project_validation_failures",
        ]
    ) else "FAIL"
    (output_path.parent / 'reasoning_validation.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (output_path.parent / 'evidence_trace.json').write_text(json.dumps(evidence_trace, indent=2), encoding='utf-8')
    ranking_audit = [result.get("ranking_audit", {}) for result in results[:20]]
    (output_path.parent / 'ranking_audit.json').write_text(json.dumps(ranking_audit, indent=2), encoding='utf-8')

    pipeline.exporter.export(results, output_path)
    print(f'Wrote {output_path} with {len(results)} rows')

    try:
        import pandas as pd

        normalized = _normalize_results(results)
        submission_df = pd.DataFrame(normalized)
        submission_df.insert(1, 'rank', range(1, len(submission_df) + 1))
        submission_df = submission_df[['candidate_id', 'rank', 'score', 'reasoning']]
        submission_df.to_excel(output_path.with_suffix('.xlsx'), index=False, engine='openpyxl')
        print(f'Wrote {output_path.with_suffix(".xlsx")}')

        rows = []
        for rank, r in enumerate(results, start=1):
            profile = r.get('explanation', {}).get('profile', {}) if isinstance(r.get('explanation', {}), dict) else {}
            rows.append({
                'Rank': rank,
                'Candidate ID': r.get('candidate_id'),
                'Current Role': profile.get('current_title') or '',
                'Years of Experience': profile.get('years_of_experience') or '',
                'Final Score': r.get('score'),
                'Semantic Score': r.get('semantic_score'),
                'Role Score': r.get('role_score'),
                'Retrieval Score': r.get('bm25_score'),
                'Behavior Score': r.get('behavior_contribution'),
                'Matched Skills': ', '.join(r.get('explanation', {}).get('strengths', [])),
                'Missing Skills': ', '.join(r.get('explanation', {}).get('concerns', [])),
                'Strengths': '; '.join(r.get('explanation', {}).get('strengths', [])),
                'Concerns': '; '.join(r.get('explanation', {}).get('concerns', [])),
                'Candidate-Specific Reasoning': r.get('reasoning', ''),
            })
        ranked_df = pd.DataFrame(rows)
        ranked_path = output_path.parent / 'ranked_candidates.xlsx'
        ranked_df.to_excel(ranked_path, index=False, engine='openpyxl')
        print(f'Wrote {ranked_path}')
    except Exception as exc:
        print(f'Workbook generation skipped: {exc}')


if __name__ == '__main__':
    jd = "Senior Python backend engineer with FAISS, vector databases, retrieval, ranking, and production ML experience"
    generate(jd)
