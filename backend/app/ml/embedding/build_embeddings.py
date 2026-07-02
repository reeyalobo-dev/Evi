from app.ml.embedding.service import EmbeddingService
from app.ml.pipeline.ranking_pipeline import RankingPipeline


def build_embeddings():
    pipeline = RankingPipeline()
    candidates = pipeline.candidates
    emb = EmbeddingService()
    print(f"Building embeddings for {len(candidates)} candidates")
    emb.ensure_candidate_embeddings(candidates)


if __name__ == '__main__':
    build_embeddings()
    print("Embeddings build complete")
