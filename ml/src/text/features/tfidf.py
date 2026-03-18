from __future__ import annotations

from typing import Any, Dict, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer


def build_tfidf_vectorizer(params: Dict[str, Any]) -> TfidfVectorizer:
    return TfidfVectorizer(
        lowercase=params.get("lowercase", True),
        strip_accents=params.get("strip_accents", "unicode"),
        ngram_range=tuple(params.get("ngram_range", [1, 1])),
        min_df=params.get("min_df", 1),
        max_df=params.get("max_df", 1.0),
        max_features=params.get("max_features"),
        sublinear_tf=params.get("sublinear_tf", False),
    )


def fit_transform_tfidf(
    train_texts,
    val_texts,
    test_texts,
    params: Dict[str, Any],
) -> Tuple[TfidfVectorizer, Any, Any, Any]:
    vectorizer = build_tfidf_vectorizer(params)
    x_train = vectorizer.fit_transform(train_texts)
    x_val = vectorizer.transform(val_texts)
    x_test = vectorizer.transform(test_texts)
    return vectorizer, x_train, x_val, x_test
