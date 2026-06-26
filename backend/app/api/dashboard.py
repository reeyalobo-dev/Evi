from flask_restx import Namespace, Resource

dashboard_ns = Namespace("dashboard", description="Dashboard statistics and KPIs")


@dashboard_ns.route("/stats")
class DashboardStats(Resource):
    def get(self):
        return {
            "total_jobs": 24,
            "active_rankings": 8,
            "top_candidates": 12,
            "model_status": "healthy",
        }


@dashboard_ns.route("/recent-activity")
class RecentActivity(Resource):
    def get(self):
        return [{"id": 1, "event": "Ranking completed", "timestamp": "2026-06-27T10:00:00Z"}]
