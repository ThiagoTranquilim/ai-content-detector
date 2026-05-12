import argparse
import re
from pathlib import Path

import joblib
import pandas as pd


DEFAULT_MODEL_PATH = "artifacts/models/text_baseline.joblib"
DEFAULT_VECTORIZER_PATH = "artifacts/vectorizers/tfidf_vectorizer.joblib"


def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s.,!?;:()/%-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def load_artifacts(model_path: str, vectorizer_path: str):
    model_path = Path(model_path)
    vectorizer_path = Path(vectorizer_path)

    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")

    if not vectorizer_path.exists():
        raise FileNotFoundError(f"Vetorizador não encontrado: {vectorizer_path}")

    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)

    return model, vectorizer


def predict_text(text: str, model, vectorizer) -> dict:
    cleaned_text = clean_text(text)

    if len(cleaned_text) < 20:
        raise ValueError("Texto muito curto para classificação confiável.")

    X = vectorizer.transform([cleaned_text])

    probabilities = model.predict_proba(X)[0]

    human_probability = float(probabilities[0])
    ai_probability = float(probabilities[1])

    threshold = 0.70
    prediction = 1 if ai_probability >= threshold else 0

    if prediction == 1:
        confidence = ai_probability
    else:
        confidence = human_probability

    if confidence >= 0.75:
        confidence_level = "alto"
    elif confidence >= 0.60:
        confidence_level = "médio"
    else:
        confidence_level = "baixo"

    return {
        "predicted_class": "ia" if prediction == 1 else "humano",
        "predicted_label": prediction,
        "human_probability": human_probability,
        "ai_probability": ai_probability,
        "confidence": confidence,
        "confidence_level": confidence_level,
        "cleaned_text": cleaned_text,
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--text",
        required=True,
        help="Texto que será classificado.",
    )

    parser.add_argument(
        "--model-path",
        default=DEFAULT_MODEL_PATH,
    )

    parser.add_argument(
        "--vectorizer-path",
        default=DEFAULT_VECTORIZER_PATH,
    )

    args = parser.parse_args()

    model, vectorizer = load_artifacts(args.model_path, args.vectorizer_path)

    result = predict_text(args.text, model, vectorizer)

    print("\nResultado da classificação:")
    print(f"Classe prevista: {result['predicted_class']}")
    print(f"Label prevista: {result['predicted_label']}")
    print(f"Probabilidade humano: {result['human_probability']:.4f}")
    print(f"Probabilidade IA: {result['ai_probability']:.4f}")
    print("Limite para IA: 0.70")
    print(f"Confiança: {result['confidence']:.4f}")
    print(f"Nível de confiança: {result['confidence_level']}")


if __name__ == "__main__":
    main()