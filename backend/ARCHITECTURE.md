# EviRank-X Backend Architecture

The backend is organized as a modular Flask application with namespace-based API groups:

- Authentication: login, register, refresh, logout
- Jobs: job creation, analysis, update, deletion
- Candidates: CRUD, upload, search
- Ranking: workflow execution and history
- Analytics: KPI and performance metrics
- Dashboard: statistics and activity streams
- Explainability: SHAP-style explanation payloads
- Supporting modules: search, uploads, reports, evidence, compare, settings, notifications

The app is designed so each domain module can evolve independently while preserving stable API contracts.
