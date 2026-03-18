from __future__ import annotations

import re

import pandas as pd


def normalize_text(text: str) -> str:
    text = str(text)
    text = text.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_text_dataframe(
    df: pd.DataFrame,
    text_column: str,
    label_column: str,
    min_text_length: int = 1,
    drop_duplicates: bool = True,
) -> pd.DataFrame:
    cleaned = df.copy()

    cleaned = cleaned.dropna(subset=[text_column, label_column])
    cleaned[text_column] = cleaned[text_column].astype(str).apply(normalize_text)
    cleaned[label_column] = cleaned[label_column].astype(int)

    cleaned = cleaned[cleaned[text_column].str.len() >= min_text_length]

    if drop_duplicates:
        cleaned = cleaned.drop_duplicates(subset=[text_column, label_column])

    valid_labels = {0, 1}
    invalid_mask = ~cleaned[label_column].isin(valid_labels)
    if invalid_mask.any():
        invalid_values = cleaned.loc[invalid_mask, label_column].unique().tolist()
        raise ValueError(f"Labels inválidos encontrados: {invalid_values}. Use apenas 0 ou 1.")

    cleaned = cleaned.reset_index(drop=True)
    return cleaned
