from flask_restx import Namespace, Resource, fields

jobs_ns = Namespace("jobs", description="Job description and analysis operations")

job_model = jobs_ns.model("Job", {
    "title": fields.String(required=True),
    "company": fields.String(required=True),
    "description": fields.String(required=True),
})


@jobs_ns.route("")
class Jobs(Resource):
    @jobs_ns.expect(job_model)
    def post(self):
        return {"id": 1, "status": "created", "analysis": {"intent": "backend engineer", "required_skills": ["python", "flask"]}}

    def get(self):
        return [{"id": 1, "title": "Senior Backend Engineer", "company": "EviRank-X"}]


@jobs_ns.route("/<int:job_id>")
class JobDetail(Resource):
    def put(self, job_id):
        return {"id": job_id, "status": "updated"}

    def delete(self, job_id):
        return {"message": "deleted"}


@jobs_ns.route("/analyze")
class AnalyzeJob(Resource):
    @jobs_ns.expect(job_model)
    def post(self):
        return {"intent": "backend engineer", "technical_requirements": ["python", "flask"], "required_skills": ["python"]}
