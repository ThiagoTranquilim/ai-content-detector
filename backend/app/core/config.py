from pathlib import Path
import os

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent

DEFAULT_TEXT_MODEL_PATH = (
    PROJECT_ROOT / "ml" / "artifacts" / "models" / "text_baseline.joblib"
)

DEFAULT_VECTORIZER_PATH = (
    PROJECT_ROOT / "ml" / "artifacts" / "vectorizers" / "tfidf_vectorizer.joblib"
)

TEXT_MODEL_PATH = Path(
    os.getenv("TEXT_MODEL_PATH", str(DEFAULT_TEXT_MODEL_PATH))
)

VECTORIZER_PATH = Path(
    os.getenv("VECTORIZER_PATH", str(DEFAULT_VECTORIZER_PATH))
)

USE_MOCK_INFERENCE = os.getenv("USE_MOCK_INFERENCE", "false").lower() == "true"

IA_THRESHOLD = float(os.getenv("IA_THRESHOLD", "0.93"))