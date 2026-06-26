from flask_restx import Namespace, Resource

ranking_ns = Namespace("ranking", description="Ranking workflow and results")


@ranking_ns.route("/run")
class RunRanking(Resource):
    def post(self):
        return {"job_id": 1, "status": "queued", "top_candidates": [{"id": 1, "score": 0.92}]}


@ranking_ns.route("/history")
class RankingHistory(Resource):
    def get(self):
        return [{"id": 1, "job_id": 1, "created_at": "2026-06-27"}]


@ranking_ns.route("/results/<int:job_id>")
class RankingResults(Resource):
    def get(self, job_id):
        return {"job_id": job_id, "results": [{"id": 1, "score": 0.94}]}
