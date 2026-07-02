import json
from pathlib import Path
from typing import Dict, List
from app.ml.export.csv_exporter import CSVExporter
from app.ml.export.reporting import ReportGenerator
from app.ml.pipeline.ranking_pipeline import RankingPipeline
from India_runs_data_and_ai_challenge.validate_submission import validate_submission


def generate_submission_with_reports(job_description: str, submission_path: str = "submission.csv", output_dir: str = "results") -> Dict[str, object]:
    pipeline = RankingPipeline()
    results = pipeline.run(job_description)
    pipeline.exporter.export(results, submission_path)

    report_gen = ReportGenerator(output_dir=output_dir)
    report_gen.write_submission_report(results)

    validation_errors = validate_submission(submission_path)
    report_gen.write_validation_report(validation_errors)

    report_gen.write_behavior_reasoning_report(_build_behavior_report(results))

    dataset_report = _build_dataset_report(pipeline.candidates)
    report_gen.write_dataset_report(dataset_report)

    return {
        "submission_path": submission_path,
        "validation_errors": validation_errors,
        "dataset_report_path": str(Path(output_dir) / "dataset_report.json"),
        "results_dir": output_dir,
    }


def _build_dataset_report(candidates: List[Dict[str, object]]) -> Dict[str, object]:
    total = len(candidates)
    with_skills = sum(1 for c in candidates if c.get("skills"))
    with_career = sum(1 for c in candidates if c.get("career_history"))
    avg_experience = sum(float(c.get("profile", {}).get("years_of_experience", 0) or 0) for c in candidates) / max(1, total)
    return {
        "total_candidates": total,
        "candidates_with_skills": with_skills,
        "candidates_with_career_history": with_career,
        "average_years_of_experience": round(avg_experience, 2),
    }

def _build_behavior_report(results: List[Dict[str, object]]) -> Dict[str, object]:
    report_items = []
    for item in results[:100]:
        report_items.append({
            "candidate_id": item.get("candidate_id"),
            "score": item.get("score"),
            "reasoning": item.get("reasoning"),
            "behavior_trace": item.get("behavior_trace", {}),
            "strengths": item.get("explanation", {}).get("strengths", []),
            "concerns": item.get("explanation", {}).get("concerns", []),
        })
    return {
        "generated_candidates": len(report_items),
        "top_candidate": report_items[0]["candidate_id"] if report_items else None,
        "items": report_items,
    }


if __name__ == "__main__":
    jd = "Senior Python backend engineer with FAISS, vector databases, retrieval, ranking, and production ML experience"
    result = generate_submission_with_reports(jd)
    print(json.dumps(result, indent=2))
