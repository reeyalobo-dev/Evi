from flask_restx import Namespace, Resource

shap_ns = Namespace("shap", description="SHAP explanation endpoints")


@shap_ns.route("/candidate/<int:candidate_id>")
class CandidateShap(Resource):
    def get(self, candidate_id):
        return {"candidate_id": candidate_id, "plot_type": "waterfall", "top_features": ["python", "flask"]}
