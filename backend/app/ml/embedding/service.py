import json
import os
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np


class EmbeddingService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.cache_dir = Path(__file__).resolve().parents[2] / "embeddings"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except Exception:
                SentenceTransformer = None
            if SentenceTransformer is None:
                self._model = None
            else:
                self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed_text(self, text: str) -> np.ndarray:
        model = self._get_model()
        if model is None:
            return np.zeros(384, dtype=np.float32)
        vector = model.encode([text], normalize_embeddings=True)[0]
        return np.asarray(vector, dtype=np.float32)

    def embed_candidate(self, candidate: Dict[str, object]) -> np.ndarray:
        text = self._candidate_text(candidate)
        return self.embed_text(text)

    def _candidate_text(self, candidate: Dict[str, object]) -> str:
        profile = candidate.get("profile", {})
        skills = [skill.get("name", "") for skill in candidate.get("skills", []) if isinstance(skill, dict)]
        career = " ".join(item.get("description", "") for item in candidate.get("career_history", []) if isinstance(item, dict))
        return " ".join([profile.get("headline", ""), profile.get("summary", ""), " ".join(skills), career])

    def ensure_candidate_embeddings(self, candidates: List[Dict[str, object]]) -> Dict[str, np.ndarray]:
        vectors = {}
        for candidate in candidates:
            candidate_id = candidate.get("candidate_id")
            path = self.cache_dir / f"{candidate_id}.npy"
            if path.exists():
                vectors[candidate_id] = np.load(path)
            else:
                vector = self.embed_candidate(candidate)
                np.save(path, vector)
                vectors[candidate_id] = vector
        return vectors
