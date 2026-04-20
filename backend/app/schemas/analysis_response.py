from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class AnalysisResponse(BaseModel):
    predicted_class: Literal["humano", "ia"] = Field(
        ...,
        description="Classe prevista pelo modelo.",
        examples=["humano"],
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Score probabilístico da predição.",
        examples=[0.87],
    )
    confidence_level: Literal["baixo", "médio", "alto"] = Field(
        ...,
        description="Nível textual de confiança associado ao score.",
        examples=["alto"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "predicted_class": "humano",
                "score": 0.87,
                "confidence_level": "alto",
            }
        }
    )