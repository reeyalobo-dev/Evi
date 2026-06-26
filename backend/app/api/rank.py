from flask_restx import Namespace, Resource, fields

from app.ml.pipeline.ranking_pipeline import RankingPipeline

rank_ns = Namespace("rank", description="Real-time ranking endpoints")

rank_model = rank_ns.model("RankRequest", {
    "job_description": fields.String(required=True),
})


@rank_ns.route("")
class Rank(Resource):
    @rank_ns.expect(rank_model)
    def post(self):
        payload = rank_ns.payload or {}
        job_description = payload.get("job_description", "")
        pipeline = RankingPipeline()
        results = pipeline.run(job_description)
        return {"top_candidates": results[:100], "count": len(results)}
