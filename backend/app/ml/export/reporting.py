import json
from pathlib import Path
from typing import List, Dict


class ReportGenerator:
    def __init__(self, output_dir: str | Path = "results") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_submission_report(self, results: List[Dict[str, object]]) -> Path:
        report = {
            "candidate_count": len(results),
            "top_candidate": results[0]["candidate_id"] if results else None,
            "top_score": float(results[0]["score"]) if results else None,
            "ranked_scores": [float(item["score"]) for item in results[:100]],
        }
        path = self.output_dir / "submission_report.json"
        path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return path

    def write_validation_report(self, errors: List[str]) -> Path:
        path = self.output_dir / "validation_report.json"
        path.write_text(json.dumps({"errors": errors}, indent=2), encoding="utf-8")
        return path

    def write_dataset_report(self, summary: Dict[str, object]) -> Path:
        path = self.output_dir / "dataset_report.json"
        path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        return path

    def write_behavior_reasoning_report(self, report_data: Dict[str, object]) -> Path:
        path = self.output_dir / "behavior_reasoning_report.json"
        path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")
        return path
