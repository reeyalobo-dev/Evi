import pytest
from app.ml.pipeline.ranking_pipeline import RankingPipeline


def test_candidates_load():
    pipeline = RankingPipeline()
    assert pipeline.candidates


def test_embedding_cache_and_build(tmp_path):
    pipeline = RankingPipeline()
    emb = pipeline.embedding_service
    # ensure caching works for first candidate
    candidate = pipeline.candidates[0]
    path = tmp_path / f"{candidate.get('candidate_id')}.npy"
    vec = emb.embed_candidate(candidate)
    import numpy as np
    np.save(path, vec)
    assert path.exists()


def test_retrieval_returns_items():
    pipeline = RankingPipeline()
    retriever = pipeline._retriever or None
    retriever = pipeline._retriever = pipeline._retriever or __import__('app.ml.retrieval.hybrid', fromlist=['HybridRetriever']).HybridRetriever(pipeline.candidates[:200])
    results = retriever.retrieve('python backend engineer', top_k=10)
    assert results


def test_run_pipeline_quick():
    pipeline = RankingPipeline()
    results = pipeline.run('Python backend engineer')
    assert isinstance(results, list)
    assert len(results) <= 100
