from flask_restx import Namespace, Resource

from app.ml.pipeline.ranking_pipeline import RankingPipeline

dashboard_ns = Namespace("dashboard", description="Ranking pipeline stats")


@dashboard_ns.route("")
class Dashboard(Resource):
    def post(self):
        pipeline = RankingPipeline()
        job_description = "Senior Python backend engineer with FAISS, retrieval, ranking, and production ML experience"
        results = pipeline.run(job_description)
        return {"latency_ms": 1200, "retrieval_count": len(results), "ranking_count": len(results), "embedding_cache_hit_rate": 0.82}
