from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SPLITS_DIR = DATA_DIR / "splits"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
MODELS_DIR = ARTIFACTS_DIR / "models"
VECTORIZERS_DIR = ARTIFACTS_DIR / "vectorizers"
REPORTS_DIR = ARTIFACTS_DIR / "reports"


def ensure_directories() -> None:
    for path in [
        DATA_DIR,
        RAW_DIR,
        SPLITS_DIR,
        ARTIFACTS_DIR,
        MODELS_DIR,
        VECTORIZERS_DIR,
        REPORTS_DIR,
    ]:
        path.mkdir(parents=True, exist_ok=True)
