import yaml
from pathlib import Path
from typing import Dict, Any

_CONFIG_PATH = Path(__file__).resolve().parents[2].parents[1] / "config" / "reasoning.yaml"


def _load_config() -> Dict[str, Any]:
    if not _CONFIG_PATH.exists():
        return {}
    with _CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def normalize_contribution(value: float, total: float) -> float:
    if total <= 0:
        return 0.0
    return abs(value) / total


class BehavioralAttributor:
    def __init__(self) -> None:
        self.config = _load_config().get("behavioral_attribution", {})
        self.enabled = bool(self.config.get("enabled", False))
        self.threshold = float(self.config.get("contribution_threshold", 0.05))
        self.supported_signals = set(self.config.get("supported_signals", []))

    def attribute(self, candidate: Dict[str, object], evidence: Dict[str, object], feature_contributions: Dict[str, float], ranking_metadata: Dict[str, object]) -> Dict[str, object]:
        attribution = {}
        total_contribution = sum(abs(value) for value in feature_contributions.values()) or 1.0
        signals = candidate.get("redrob_signals", {}) or {}

        behavior_contribution = float(feature_contributions.get("behavior_score", 0.0) or 0.0)
        normalized = normalize_contribution(behavior_contribution, total_contribution)
        used_by_model = abs(behavior_contribution) > 0.0
        meets_threshold = normalized >= self.threshold

        for signal in self.supported_signals:
            present = signal in signals and signals[signal] is not None
            included_in_evidence = signal in evidence.get("behavior_evidence", {}).get("signals", {})
            included = all([present, included_in_evidence, used_by_model, meets_threshold, self.enabled])

            attribution[signal] = {
                "value": signals.get(signal),
                "contribution": behavior_contribution,
                "normalized_contribution": round(normalized, 4),
                "included": included,
                "reason": "Contribution exceeded configured threshold" if included else "Not included due to threshold, absence, or zero contribution",
            }

        return attribution
