from flask_restx import Namespace, Resource, fields

candidates_ns = Namespace("candidates", description="Candidate management and upload")

candidate_model = candidates_ns.model("Candidate", {
    "name": fields.String(required=True),
    "email": fields.String(required=True),
    "skills": fields.List(fields.String),
})


@candidates_ns.route("")
class Candidates(Resource):
    @candidates_ns.expect(candidate_model)
    def post(self):
        return {"id": 1, "status": "created"}

    def get(self):
        return [{"id": 1, "name": "Ava Chen", "skills": ["python", "flask"]}]


@candidates_ns.route("/upload")
class UploadCandidates(Resource):
    def post(self):
        return {"message": "upload queued"}


@candidates_ns.route("/search")
class SearchCandidates(Resource):
    def get(self):
        return [{"id": 1, "name": "Ava Chen"}]
