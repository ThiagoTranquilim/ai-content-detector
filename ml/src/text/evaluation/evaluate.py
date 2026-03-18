from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import numpy as np

from src.common.metrics import compute_classification_metrics


def evaluate_predictions(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray | None = None,
) -> Dict[str, Any]:
    return compute_classification_metrics(y_true=y_true, y_pred=y_pred, y_proba=y_proba)


def save_metrics(metrics: Dict[str, Any], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
