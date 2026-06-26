from app import create_app
from app.ml.pipeline.ranking_pipeline import RankingPipeline


def test_intent_extraction_produces_structured_output():
    pipeline = RankingPipeline()
    intent = pipeline.intent_extractor.extract("Senior Python backend engineer with FAISS, vector databases, retrieval, ranking, and production ML experience")
    assert intent["required_skills"]
    assert intent["preferred_skills"]
    assert intent["experience_years"] >= 0


def test_pipeline_returns_top_candidates():
    pipeline = RankingPipeline()
    results = pipeline.run("Senior Python backend engineer with FAISS, retrieval, ranking, and production ML experience")
    assert len(results) >= 10
    assert all("candidate_id" in item for item in results)


def test_export_creates_submission_csv(tmp_path):
    pipeline = RankingPipeline()
    results = pipeline.run("Senior Python backend engineer with FAISS, retrieval, ranking, and production ML experience")
    out_path = tmp_path / "submission.csv"
    pipeline.exporter.export(results, out_path)
    assert out_path.exists()
    assert out_path.stat().st_size > 0


def test_api_rank_endpoint():
    app = create_app()
    client = app.test_client()
    response = client.post("/api/rank", json={"job_description": "Senior Python engineer with vector databases and ranking systems"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["top_candidates"]
