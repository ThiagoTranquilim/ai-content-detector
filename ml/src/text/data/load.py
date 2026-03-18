from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_text_dataset(
    csv_path: str | Path,
    text_column: str,
    label_column: str,
) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset não encontrado: {path}")

    df = pd.read_csv(path)

    missing_columns = [col for col in [text_column, label_column] if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Colunas obrigatórias ausentes no dataset: {missing_columns}. "
            f"Colunas encontradas: {list(df.columns)}"
        )

    return df[[text_column, label_column]].copy()
