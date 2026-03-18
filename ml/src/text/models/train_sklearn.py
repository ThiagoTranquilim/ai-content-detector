from __future__ import annotations

from typing import Any, Dict, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression


def train_logistic_regression(
    x_train: Any,
    y_train: np.ndarray,
    params: Dict[str, Any],
) -> LogisticRegression:
    model = LogisticRegression(
        C=params.get("C", 1.0),
        max_iter=params.get("max_iter", 1000),
        class_weight=params.get("class_weight"),
        solver=params.get("solver", "liblinear"),
        random_state=params.get("random_state", 42),
    )
    model.fit(x_train, y_train)
    return model


def predict_with_model(model: Any, x_data: Any) -> Tuple[np.ndarray, np.ndarray]:
    y_pred = model.predict(x_data)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(x_data)[:, 1]
    else:
        y_proba = None
    return y_pred, y_proba
