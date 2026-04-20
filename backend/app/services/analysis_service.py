from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, TypedDict

from app.schemas import AnalysisResponse


PredictedClass = Literal["humano", "ia"]
ConfidenceLevel = Literal["baixo", "médio", "alto"]


class InferenceResult(TypedDict):
    predicted_class: PredictedClass
    score: float
    confidence_level: ConfidenceLevel


class TextInferenceServiceProtocol(Protocol):
    def predict(self, text: str) -> InferenceResult:
        """
        Deve receber um texto limpo e devolver:
        - predicted_class
        - score
        - confidence_level
        """
        ...


@dataclass(slots=True)
class AnalysisService:
    text_inference_service: TextInferenceServiceProtocol

    def analyze_text(self, text: str) -> AnalysisResponse:
        clean_text = self._normalize_text(text)

        if not clean_text:
            raise ValueError("O texto não pode estar vazio.")

        inference_result = self.text_inference_service.predict(clean_text)

        score = float(inference_result["score"])
        if not 0.0 <= score <= 1.0:
            raise ValueError("O score retornado pela inferência deve estar entre 0 e 1.")

        return AnalysisResponse(
            predicted_class=inference_result["predicted_class"],
            score=score,
            confidence_level=inference_result["confidence_level"],
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        """
        Remove espaços excedentes e normaliza quebras de linha/espaços.
        """
        return " ".join(text.split())