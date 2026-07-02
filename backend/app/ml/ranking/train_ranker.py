import numpy as np
from app.ml.pipeline.ranking_pipeline import RankingPipeline
from app.ml.ranking.model import LambdaMartRanker


def train_ranker():
    pipeline = RankingPipeline()
    # sample small set
    candidates = pipeline.candidates[:500]
    # build simple features
    X = []
    y = []
    for i, c in enumerate(candidates[:100]):
        evidence = pipeline.evidence_builder.build(c, {'required_skills':[],'experience_years':4}, '')
        fv = pipeline._build_feature_vector(c, {'required_skills':[],'experience_years':4}, evidence)
        X.append(fv)
        # pseudo labels from profile completeness + years
        pc = float(c.get('redrob_signals', {}).get('profile_completeness_score', 50)) / 100.0
        yrs = float(c.get('profile', {}).get('years_of_experience', 0) or 0) / 10.0
        y.append(min(0.99, 0.2 + pc * 0.6 + yrs * 0.2))
    X = np.array(X)
    y = np.array(y)
    ranker = LambdaMartRanker()
    ranker.train(X, y)
    print('Ranker trained and saved')


if __name__ == '__main__':
    train_ranker()
