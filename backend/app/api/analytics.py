from flask_restx import Namespace, Resource

analytics_ns = Namespace("analytics", description="Analytics and performance metrics")


@analytics_ns.route("")
class Analytics(Resource):
    def get(self):
        return {
            "ndcg": 0.91,
            "map": 0.88,
            "precision_at_10": 0.83,
            "latency_ms": 140,
            "cpu_usage": 41,
            "memory_mb": 612,
        }
