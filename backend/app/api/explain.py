from flask_restx import Namespace, Resource

explain_ns = Namespace("explain", description="Candidate explanation endpoints")


@explain_ns.route("/<candidate_id>")
class Explain(Resource):
    def get(self, candidate_id):
        return {"candidate_id": candidate_id, "summary": "Technical fit explanation generated from evidence and ranking features."}
