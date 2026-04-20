from fastapi import APIRouter, HTTPException, status

from app.schemas import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import AnalysisService
from app.services.text_inference_service import build_text_inference_service

router = APIRouter(
    prefix="/analises",
    tags=["analises"],
)

analysis_service = AnalysisService(
    text_inference_service=build_text_inference_service()
)


@router.post(
    "/texto",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Submeter texto para análise",
)
async def analyze_text(payload: AnalysisRequest) -> AnalysisResponse:
    try:
        return analysis_service.analyze_text(payload.text)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except NotImplementedError as exc:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=str(exc),
        ) from exc

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc