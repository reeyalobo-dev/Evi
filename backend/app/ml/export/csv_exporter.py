import csv
from pathlib import Path
from typing import List, Dict


class CSVExporter:
    def export(self, results: List[Dict[str, object]], output_path: str | Path) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["candidate_id", "rank", "score", "reasoning"])
            for idx, result in enumerate(results[:100], start=1):
                writer.writerow([result.get("candidate_id"), idx, round(float(result.get("score", 0.0)), 4), result.get("reasoning", "")])
        return path
