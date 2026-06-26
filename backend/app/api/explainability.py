from flask_restx import Namespace, Resource

explainability_ns = Namespace("explainability", description="Explainability and SHAP outputs")


@explainability_ns.route("/candidate/<int:candidate_id>")
class CandidateExplanation(Resource):
    def get(self, candidate_id):
        return {
            "candidate_id": candidate_id,
            "summary": "Strong backend engineering match with relevant Python and Flask experience.",
            "features": [
                {"name": "python", "weight": 0.31},
                {"name": "flask", "weight": 0.18},
            ],
        }
