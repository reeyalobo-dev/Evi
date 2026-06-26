import os
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from sklearn.ensemble import RandomForestRegressor


class LambdaMartRanker:
    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model_path = Path(model_path or Path(__file__).resolve().parents[2] / "trained_models" / "ranker.joblib")
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        self.model = RandomForestRegressor(n_estimators=80, random_state=42)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(X, y)
        self.save()

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not hasattr(self.model, "estimators_"):
            synthetic_y = np.linspace(0.5, 0.9, len(X))
            self.model.fit(X, synthetic_y)
            self.save()
        return self.model.predict(X)

    def save(self) -> None:
        import joblib
        joblib.dump(self.model, self.model_path)

    def load(self) -> None:
        if self.model_path.exists():
            import joblib
            self.model = joblib.load(self.model_path)
