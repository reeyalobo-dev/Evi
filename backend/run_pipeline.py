import time
import json
from pathlib import Path
from time import perf_counter

from app.ml.pipeline.ranking_pipeline import RankingPipeline
from app.ml.embedding.build_embeddings import build_embeddings
from app.ml.retrieval.build_index import build_index
from app.ml.ranking.train_ranker import train_ranker
from app.ml.export.generate_submission import generate


def run_demo(job_description: str):
    start = perf_counter()
    print('Starting EviRank-X demo pipeline...')
    # Ensure embeddings
    emb_dir = Path(__file__).resolve().parent / 'app' / 'ml' / 'embeddings'
    if not emb_dir.exists() or not any(emb_dir.glob('*.npy')):
        print('Embeddings not found, building...')
        build_embeddings()
    else:
        print('Embeddings found, skipping build')

    # Ensure index
    idx_file = Path('faiss_index.joblib')
    if not idx_file.exists():
        print('Index not found, building...')
        build_index()
    else:
        print('Index found, skipping build')

    # Ensure ranker model
    model_file = Path(__file__).resolve().parent / 'app' / 'ml' / 'trained_models' / 'ranker.joblib'
    if not model_file.exists():
        print('Ranker model not found, training...')
        train_ranker()
    else:
        print('Ranker found, skipping training')

    # Run ranking and export
    generate(job_description, 'submission.csv')

    elapsed = (perf_counter() - start)
    print(f'Demo complete in {elapsed:.1f}s')

    # Basic reports
    pipeline = RankingPipeline()
    results = pipeline.run(job_description)
    # Retrieval report
    retrieval = []
    for i, r in enumerate(results[:100], start=1):
        retrieval.append({'rank': i, 'candidate_id': r['candidate_id'], 'score': r['score'], 'reason': r.get('reasoning','')})
    Path('retrieval_report.json').write_text(json.dumps(retrieval, indent=2))
    print('Wrote retrieval_report.json')

    # Ranking report with detailed statistics and distributions
    import statistics
    scores = [r.get('score', 0.0) for r in results]
    duplicates = len(scores) - len(set(scores))
    top100 = scores[:100]
    hist = []
    bins = []
    try:
        import numpy as np
        hist_vals, bin_edges = np.histogram(top100, bins=10)
        hist = hist_vals.tolist()
        bins = [float(b) for b in bin_edges.tolist()]
    except Exception:
        pass

    ranking_report = {
        'count': len(results),
        'top_score': results[0]['score'] if results else None,
        'min': min(scores) if scores else None,
        'max': max(scores) if scores else None,
        'mean': statistics.mean(scores) if scores else None,
        'median': statistics.median(scores) if scores else None,
        'stdev': statistics.pstdev(scores) if scores else None,
        'duplicate_scores': duplicates,
        'top100_histogram': {'bins': bins, 'counts': hist},
    }
    Path('ranking_report.json').write_text(json.dumps(ranking_report, indent=2))
    # score distribution for external analysis
    score_dist = {
        'min': ranking_report['min'],
        'max': ranking_report['max'],
        'mean': ranking_report['mean'],
        'median': ranking_report['median'],
        'stdev': ranking_report['stdev'],
        'duplicate_scores': duplicates,
    }
    Path('results').mkdir(exist_ok=True)
    Path('results/score_distribution.json').write_text(json.dumps(score_dist, indent=2))
    print('Wrote ranking_report.json and results/score_distribution.json')


if __name__ == '__main__':
    jd = 'Senior Python backend engineer with FAISS, vector databases, retrieval, ranking, and production ML experience'
    run_demo(jd)
