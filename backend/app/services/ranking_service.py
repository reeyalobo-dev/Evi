class RankingService:
    def run(self, job_payload: dict) -> dict:
        return {
            "job_id": job_payload.get("id", 1),
            "status": "completed",
            "top_candidates": [{"id": 1, "score": 0.93, "confidence": "high"}],
        }
