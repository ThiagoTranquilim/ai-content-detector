from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import joblib

from src.text.data.clean import normalize_text


@dataclass
class TextPrediction:
    predicted_label: int
    predicted_class: str
    probability_human: float
    probability_ai: float
    confidence: float


def load_inference_artifacts(model_path: str, vectorizer_path: str) -> tuple[Any, Any]:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer


def predict_text(text: str, model: Any, vectorizer: Any) -> TextPrediction:
    normalized = normalize_text(text)
    x = vectorizer.transform([normalized])

    if not hasattr(model, "predict_proba"):
        raise ValueError("O modelo carregado não expõe predict_proba().")

    probabilities = model.predict_proba(x)[0]
    probability_human = float(probabilities[0])
    probability_ai = float(probabilities[1])

    predicted_label = int(probability_ai >= 0.5)
    predicted_class = "ai" if predicted_label == 1 else "human"
    confidence = max(probability_human, probability_ai)

    return TextPrediction(
        predicted_label=predicted_label,
        predicted_class=predicted_class,
        probability_human=probability_human,
        probability_ai=probability_ai,
        confidence=float(confidence),
    )
