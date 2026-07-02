import csv
from pathlib import Path
from typing import List, Dict


class CSVExporter:
    def export(self, results: List[Dict[str, object]], output_path: str | Path) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        normalized = []
        for result in results[:100]:
            # format final score to 6 decimals for export, keep internal precision in memory
            score = float(result.get("score", 0.0))
            score = float(f"{score:.6f}")
            normalized.append({
                "candidate_id": result.get("candidate_id"),
                "score": score,
                "reasoning": result.get("reasoning", ""),
            })
        normalized.sort(key=lambda item: (-item["score"], str(item.get("candidate_id", ""))))
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["candidate_id", "rank", "score", "reasoning"])
            for idx, result in enumerate(normalized, start=1):
                writer.writerow([result["candidate_id"], idx, result["score"], result["reasoning"]])
        return path
