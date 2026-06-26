from flask_restx import Namespace, Resource

uploads_ns = Namespace("uploads", description="Resume and document upload endpoints")


@uploads_ns.route("")
class Uploads(Resource):
    def post(self):
        return {"message": "upload accepted"}
