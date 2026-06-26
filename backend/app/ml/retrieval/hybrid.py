import math
import re
from collections import Counter
from typing import Dict, List, Tuple

from rank_bm25 import BM25Okapi


class HybridRetriever:
    def __init__(self, candidates: List[Dict[str, object]]) -> None:
        self.candidates = candidates
        self.corpus = [self._build_text(candidate) for candidate in candidates]
        self.bm25 = BM25Okapi([self._tokenize(text) for text in self.corpus])

    def _build_text(self, candidate: Dict[str, object]) -> str:
        profile = candidate.get("profile", {})
        skills = [skill.get("name", "") for skill in candidate.get("skills", []) if isinstance(skill, dict)]
        career = " ".join(item.get("description", "") for item in candidate.get("career_history", []) if isinstance(item, dict))
        return " ".join([profile.get("headline", ""), profile.get("summary", ""), " ".join(skills), career])

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-z0-9+.#-]+", text.lower())

    def retrieve(self, job_description: str, top_k: int = 2000) -> List[Tuple[int, float, Dict[str, object]]]:
        tokens = self._tokenize(job_description)
        bm25_scores = self.bm25.get_scores(tokens)
        ranked = sorted(enumerate(bm25_scores), key=lambda item: item[1], reverse=True)[:top_k]
        return [(idx, score, self.candidates[idx]) for idx, score in ranked if score > 0]
