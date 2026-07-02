import joblib
from pathlib import Path
from typing import List

from app.ml.pipeline.ranking_pipeline import RankingPipeline


def build_index():
    pipeline = RankingPipeline()
    candidates = pipeline.candidates
    # load embeddings from the same cache directory as the embedding service
    emb_dir = Path(__file__).resolve().parents[2] / "embeddings"
    emb_dir.mkdir(parents=True, exist_ok=True)
    vectors = []
    ids = []
    for c in candidates:
        cid = c.get('candidate_id')
        path = emb_dir / f"{cid}.npy"
        if path.exists():
            import numpy as np
            vectors.append(np.load(path))
            ids.append(cid)
    if not vectors:
        raise RuntimeError('No candidate embeddings found. Run build_embeddings first.')
    X = vectors
    try:
        import faiss
        index = faiss.IndexFlatIP(len(X[0]))
        import numpy as np
        matrix = np.vstack(X).astype('float32')
        faiss.normalize_L2(matrix)
        index.add(matrix)
        joblib.dump({'type':'faiss','index':index, 'ids': ids}, 'faiss_index.joblib')
        print('FAISS index built')
    except Exception:
        # fallback to sklearn neighbor index
        from sklearn.neighbors import NearestNeighbors
        import numpy as np
        matrix = np.vstack(X)
        nn = NearestNeighbors(n_neighbors=50, metric='cosine')
        nn.fit(matrix)
        joblib.dump({'type':'sklearn','index':nn, 'ids': ids}, 'faiss_index.joblib')
        print('Sklearn index built as fallback')


if __name__ == '__main__':
    build_index()
