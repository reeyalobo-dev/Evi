from app.api.auth import auth_ns
from app.api.jobs import jobs_ns
from app.api.candidates import candidates_ns
from app.api.ranking import ranking_ns
from app.api.analytics import analytics_ns
from app.api.dashboard import dashboard_ns
from app.api.explainability import explainability_ns
from app.api.search import search_ns
from app.api.uploads import uploads_ns
from app.api.settings import settings_ns
from app.api.notifications import notifications_ns
from app.api.reports import reports_ns
from app.api.evidence import evidence_ns
from app.api.shap import shap_ns
from app.api.compare import compare_ns
from app.api.rank import rank_ns
from app.api.explain import explain_ns
from app.api.export import export_ns
from app.api.dashboard_stats import dashboard_ns


def register_namespaces(api):
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(jobs_ns, path="/api/jobs")
    api.add_namespace(candidates_ns, path="/api/candidates")
    api.add_namespace(ranking_ns, path="/api/ranking")
    api.add_namespace(analytics_ns, path="/api/analytics")
    api.add_namespace(dashboard_ns, path="/api/dashboard")
    api.add_namespace(explainability_ns, path="/api/explainability")
    api.add_namespace(search_ns, path="/api/search")
    api.add_namespace(uploads_ns, path="/api/uploads")
    api.add_namespace(settings_ns, path="/api/settings")
    api.add_namespace(notifications_ns, path="/api/notifications")
    api.add_namespace(reports_ns, path="/api/reports")
    api.add_namespace(evidence_ns, path="/api/evidence")
    api.add_namespace(shap_ns, path="/api/shap")
    api.add_namespace(compare_ns, path="/api/compare")
    api.add_namespace(rank_ns, path="/api/rank")
    api.add_namespace(explain_ns, path="/api/explain")
    api.add_namespace(export_ns, path="/api/export")
    api.add_namespace(dashboard_ns, path="/api/dashboard")
