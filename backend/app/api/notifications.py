from flask_restx import Namespace, Resource

notifications_ns = Namespace("notifications", description="Notifications and live updates")


@notifications_ns.route("")
class Notifications(Resource):
    def get(self):
        return [{"id": 1, "message": "Ranking completed", "read": False}]
