from flask_restx import Namespace, Resource
from flask import request

from app.ml.pipeline.ranking_pipeline import RankingPipeline

export_ns = Namespace("export", description="Submission export endpoints")


@export_ns.route("")
class Export(Resource):
    def post(self):
        payload = request.get_json(silent=True) or {}
        job_description = payload.get("job_description", "")
        pipeline = RankingPipeline()
        results = pipeline.run(job_description)
        output_path = "submission.csv"
        pipeline.exporter.export(results, output_path)
        return {"path": output_path, "count": len(results)}
