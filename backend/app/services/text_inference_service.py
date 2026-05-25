from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

import joblib

from app.core.config import TEXT_MODEL_PATH, VECTORIZER_PATH, USE_MOCK_INFERENCE, IA_THRESHOLD
from app.services.analysis_service import (
    ConfidenceLevel,
    InferenceResult,
    PredictedClass,
    TextInferenceServiceProtocol,
)


class MockTextInferenceService:
    def predict(self, text: str) -> InferenceResult:
        normalized_text = text.lower()
        if 'chatgpt' in normalized_text or 'inteligencia artificial' in normalized_text:
            return {'predicted_class': 'ia', 'score': 0.82, 'confidence_level': 'alto'}
        return {'predicted_class': 'humano', 'score': 0.76, 'confidence_level': 'medio'}


class UnconfiguredTextInferenceService:
    def predict(self, text: str) -> InferenceResult:
        raise NotImplementedError('Servico de inferencia textual ainda nao configurado.')


@dataclass(slots=True)
class SklearnTextInferenceService:
    model_path: str | Path
    vectorizer_path: str | Path
    positive_class_label: Any = 1
    model: Any = field(init=False)
    vectorizer: Any = field(init=False)

    def __post_init__(self) -> None:
        self.model = self._load_artifact(self.model_path, 'Modelo')
        self.vectorizer = self._load_artifact(self.vectorizer_path, 'Vetorizador')

    def predict(self, text: str) -> InferenceResult:
        if not hasattr(self.model, 'predict_proba'):
            raise ValueError('O modelo precisa implementar predict_proba.')
        cleaned = self._clean_text(text)
        X = self.vectorizer.transform([cleaned])
        probabilities = self.model.predict_proba(X)[0]
        classes = list(self.model.classes_)
        positive_index = self._resolve_positive_class_index(classes)
        probability_ia = float(probabilities[positive_index])
        predicted_class = self._resolve_predicted_class(probability_ia)
        score = probability_ia if predicted_class == 'ia' else 1.0 - probability_ia
        return {
            'predicted_class': predicted_class,
            'score': score,
            'confidence_level': self._to_confidence_level(score),
        }

    @staticmethod
    def _clean_text(text: str) -> str:
        text = str(text).lower()
        text = re.sub(r'http\S+|www\S+', ' ', text)
        text = re.sub(r'\S+@\S+', ' ', text)
        text = re.sub(r'<.*?>', ' ', text)
        text = re.sub(r'[^a-zA-Z\xc0-\xff0-9\s.,!?;:()/%-]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    @staticmethod
    def _load_artifact(path: str | Path, label: str) -> Any:
        artifact_path = Path(path)
        if not artifact_path.exists():
            raise FileNotFoundError(f'{label} nao encontrado em: {artifact_path}')
        return joblib.load(artifact_path)

    def _resolve_positive_class_index(self, classes: Sequence[Any]) -> int:
        for candidate in [self.positive_class_label, 'ia', 1, True]:
            if candidate in classes:
                return classes.index(candidate)
        raise ValueError(f'Classe positiva nao encontrada. Classes: {classes}')

    @staticmethod
    def _resolve_predicted_class(probability_ia: float) -> PredictedClass:
        return 'ia' if probability_ia >= IA_THRESHOLD else 'humano'

    @staticmethod
    def _to_confidence_level(score: float) -> ConfidenceLevel:
        if score < 0.60:
            return 'baixo'
        if score < 0.80:
            return 'medio'
        return 'alto'


def build_text_inference_service() -> TextInferenceServiceProtocol:
    if USE_MOCK_INFERENCE:
        return MockTextInferenceService()
    if TEXT_MODEL_PATH.exists() and VECTORIZER_PATH.exists():
        return SklearnTextInferenceService(
            model_path=TEXT_MODEL_PATH,
            vectorizer_path=VECTORIZER_PATH,
        )
    return UnconfiguredTextInferenceService()