from fastapi import FastAPI

from app.routers import analyses_router

app = FastAPI(
    title="Detector de Conteúdo IA",
    version="0.1.0",
    description="API para submissão de texto e retorno de classificação probabilística.",
)

app.include_router(analyses_router)