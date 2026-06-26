from flask_restx import Namespace, Resource

reports_ns = Namespace("reports", description="Reports and export endpoints")


@reports_ns.route("")
class Reports(Resource):
    def get(self):
        return {"report_types": ["csv", "pdf", "json"]}
