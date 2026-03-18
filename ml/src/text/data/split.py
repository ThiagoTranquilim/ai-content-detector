from __future__ import annotations

from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


def split_text_dataset(
    df: pd.DataFrame,
    label_column: str,
    train_size: float,
    val_size: float,
    test_size: float,
    seed: int,
    stratify: bool = True,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    total = round(train_size + val_size + test_size, 10)
    if total != 1.0:
        raise ValueError("A soma de train_size + val_size + test_size deve ser 1.0")

    y = df[label_column] if stratify else None

    train_df, temp_df = train_test_split(
        df,
        test_size=(1.0 - train_size),
        random_state=seed,
        stratify=y,
    )

    temp_ratio = val_size + test_size
    val_relative = val_size / temp_ratio
    y_temp = temp_df[label_column] if stratify else None

    val_df, test_df = train_test_split(
        temp_df,
        test_size=(1.0 - val_relative),
        random_state=seed,
        stratify=y_temp,
    )

    return (
        train_df.reset_index(drop=True),
        val_df.reset_index(drop=True),
        test_df.reset_index(drop=True),
    )
