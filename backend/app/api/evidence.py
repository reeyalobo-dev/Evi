from flask_restx import Namespace, Resource

evidence_ns = Namespace("evidence", description="Structured evidence endpoints")


@evidence_ns.route("/candidate/<int:candidate_id>")
class CandidateEvidence(Resource):
    def get(self, candidate_id):
        return {"candidate_id": candidate_id, "evidence": ["semantic", "career", "project"]}
