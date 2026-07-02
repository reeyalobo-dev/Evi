from pathlib import Path
from typing import Dict, List

import pandas as pd


class XLSXExporter:
    def export(self, results: List[Dict[str, object]], output_path: str | Path) -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = []
        for idx, result in enumerate(results[:100], start=1):
            rows.append({
                "candidate_id": result.get("candidate_id"),
                "rank": idx,
                "score": round(float(result.get("score", 0.0)), 4),
                "reasoning": result.get("reasoning", ""),
            })
        df = pd.DataFrame(rows)
        df.to_excel(path, index=False)
        return path
