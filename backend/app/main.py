from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyses_router

app = FastAPI(
    title="Detector de Conteúdo IA",
    version="0.1.0",
    description="API para submissão de texto e retorno de classificação probabilística.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(analyses_router)
