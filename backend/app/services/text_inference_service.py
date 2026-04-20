from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from app.core.config import TEXT_MODEL_PATH, USE_MOCK_INFERENCE
from app.services.analysis_service import (
    ConfidenceLevel,
    InferenceResult,
    PredictedClass,
    TextInferenceServiceProtocol,
)


class MockTextInferenceService:
    """
    Serviço temporário para desenvolvimento do backend/frontend
    enquanto o modelo real ainda não existe.
    """

    def predict(self, text: str) -> InferenceResult:
        normalized_text = text.lower()

        if "chatgpt" in normalized_text or "inteligência artificial" in normalized_text:
            return {
                "predicted_class": "ia",
                "score": 0.82,
                "confidence_level": "alto",
            }

        return {
            "predicted_class": "humano",
            "score": 0.76,
            "confidence_level": "médio",
        }


class UnconfiguredTextInferenceService:
    def predict(self, text: str) -> InferenceResult:
        raise NotImplementedError(
            "Serviço de inferência textual ainda não configurado."
        )


@dataclass(slots=True)
class SklearnTextInferenceService:
    model_path: str | Path
    positive_class_label: Any = 1
    model: Any = field(init=False)

    def __post_init__(self) -> None:
        self.model = self._load_model()

    def predict(self, text: str) -> InferenceResult:
        if not hasattr(self.model, "predict_proba"):
            raise ValueError(
                "O modelo textual precisa implementar predict_proba para retornar score probabilístico."
            )

        probabilities = self.model.predict_proba([text])[0]
        classes = list(self.model.classes_)
        positive_index = self._resolve_positive_class_index(classes)

        probability_ia = float(probabilities[positive_index])
        predicted_class = self._resolve_predicted_class(probability_ia)
        score = probability_ia if predicted_class == "ia" else 1.0 - probability_ia

        return {
            "predicted_class": predicted_class,
            "score": score,
            "confidence_level": self._to_confidence_level(score),
        }

    def _load_model(self) -> Any:
        model_path = Path(self.model_path)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Modelo textual não encontrado em: {model_path}"
            )

        with model_path.open("rb") as file:
            return pickle.load(file)

    def _resolve_positive_class_index(self, classes: Sequence[Any]) -> int:
        candidates = [self.positive_class_label, "ia", 1, True]

        for candidate in candidates:
            if candidate in classes:
                return classes.index(candidate)

        raise ValueError(
            f"Não foi possível identificar a classe positiva de IA. Classes encontradas: {classes}"
        )

    @staticmethod
    def _resolve_predicted_class(probability_ia: float) -> PredictedClass:
        return "ia" if probability_ia >= 0.5 else "humano"

    @staticmethod
    def _to_confidence_level(score: float) -> ConfidenceLevel:
        if score < 0.60:
            return "baixo"
        if score < 0.80:
            return "médio"
        return "alto"


def build_text_inference_service() -> TextInferenceServiceProtocol:
    if USE_MOCK_INFERENCE:
        return MockTextInferenceService()

    if TEXT_MODEL_PATH.exists():
        return SklearnTextInferenceService(model_path=TEXT_MODEL_PATH)

    return UnconfiguredTextInferenceService()