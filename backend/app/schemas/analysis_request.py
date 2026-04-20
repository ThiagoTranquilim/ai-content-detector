from pydantic import BaseModel, ConfigDict, Field


class AnalysisRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="Texto digitado ou colado para análise.",
        examples=[
            "Este é um exemplo de texto que será enviado para classificação."
        ],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Este é um exemplo de texto que será enviado para classificação."
            }
        }
    )