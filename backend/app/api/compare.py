from flask_restx import Namespace, Resource

compare_ns = Namespace("compare", description="Candidate comparison endpoints")


@compare_ns.route("")
class Compare(Resource):
    def post(self):
        return {"comparison": [{"id": 1, "score": 0.88}, {"id": 2, "score": 0.81}]}
