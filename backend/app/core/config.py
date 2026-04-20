from pathlib import Path
import os

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent

DEFAULT_TEXT_MODEL_PATH = (
    PROJECT_ROOT / "ml" / "artifacts" / "models" / "text_model.pkl"
)

TEXT_MODEL_PATH = Path(
    os.getenv("TEXT_MODEL_PATH", str(DEFAULT_TEXT_MODEL_PATH))
)

USE_MOCK_INFERENCE = os.getenv("USE_MOCK_INFERENCE", "true").lower() == "true"