import pandas as pd

from src.text.data.clean import clean_text_dataframe, normalize_text


def test_normalize_text_removes_extra_spaces():
    text = "olá\n\n mundo\t   teste"
    assert normalize_text(text) == "olá mundo teste"


def test_clean_text_dataframe_removes_nulls_short_texts_and_duplicates():
    df = pd.DataFrame(
        {
            "text": ["texto válido", None, "oi", "texto válido"],
            "label": [0, 1, 0, 0],
        }
    )

    cleaned = clean_text_dataframe(
        df=df,
        text_column="text",
        label_column="label",
        min_text_length=5,
        drop_duplicates=True,
    )

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["text"] == "texto válido"
    assert cleaned.iloc[0]["label"] == 0
