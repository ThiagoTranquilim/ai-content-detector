import argparse
import json
import re
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import yaml

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def clean_text(text: str, config: dict) -> str:
    if pd.isna(text):
        return ""

    text = str(text)

    if config.get("lowercase", True):
        text = text.lower()

    if config.get("remove_urls", True):
        text = re.sub(r"http\S+|www\S+", " ", text)

    if config.get("remove_emails", True):
        text = re.sub(r"\S+@\S+", " ", text)

    text = re.sub(r"<.*?>", " ", text)

    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s.,!?;:()/%-]", " ", text)

    if config.get("remove_extra_spaces", True):
        text = re.sub(r"\s+", " ", text).strip()

    return text


def load_and_clean_dataset(config: dict) -> pd.DataFrame:
    dataset_path = Path(config["dataset"]["path"])
    text_column = config["dataset"]["text_column"]
    label_column = config["dataset"]["label_column"]
    cleaning_config = config["cleaning"]

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset não encontrado em: {dataset_path}")

    df = pd.read_csv(dataset_path)

    required_columns = {text_column, label_column}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Colunas ausentes no CSV: {missing_columns}")

    df = df[[text_column, label_column]].copy()

    df = df.dropna(subset=[text_column, label_column])

    df[text_column] = df[text_column].apply(
        lambda value: clean_text(value, cleaning_config)
    )

    min_chars = cleaning_config.get("min_chars", 20)
    df = df[df[text_column].str.len() >= min_chars]

    df[label_column] = df[label_column].astype(int)

    df = df[df[label_column].isin([0, 1])]

    df = df.drop_duplicates(subset=[text_column])

    df = df.reset_index(drop=True)

    if df.empty:
        raise ValueError("Depois da limpeza, o dataset ficou vazio.")

    if df[label_column].nunique() < 2:
        raise ValueError("O dataset precisa ter as duas classes: 0 humano e 1 IA.")

    return df


def split_dataset(df: pd.DataFrame, config: dict):
    label_column = config["dataset"]["label_column"]

    test_size = config["split"]["test_size"]
    val_size = config["split"]["val_size"]
    random_state = config["split"]["random_state"]

    train_val_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[label_column],
    )

    adjusted_val_size = val_size / (1 - test_size)

    train_df, val_df = train_test_split(
        train_val_df,
        test_size=adjusted_val_size,
        random_state=random_state,
        stratify=train_val_df[label_column],
    )

    return train_df, val_df, test_df


def save_splits(train_df, val_df, test_df, config: dict):
    train_path = Path(config["artifacts"]["train_path"])
    val_path = Path(config["artifacts"]["val_path"])
    test_path = Path(config["artifacts"]["test_path"])

    train_path.parent.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)


def build_vectorizer(config: dict) -> TfidfVectorizer:
    vectorizer_config = config["vectorizer"]

    vectorizer = TfidfVectorizer(
        max_features=vectorizer_config["max_features"],
        ngram_range=(
            vectorizer_config["ngram_min"],
            vectorizer_config["ngram_max"],
        ),
        min_df=vectorizer_config["min_df"],
        max_df=vectorizer_config["max_df"],
        sublinear_tf=True,
    )

    return vectorizer


def build_model(config: dict) -> LogisticRegression:
    model_config = config["model"]

    model = LogisticRegression(
        max_iter=model_config["max_iter"],
        class_weight=model_config.get("class_weight", "balanced"),
        solver="liblinear",
        random_state=config["split"]["random_state"],
    )

    return model


def evaluate_model(model, X, y, dataset_name: str) -> dict:
    y_pred = model.predict(X)
    y_proba = model.predict_proba(X)[:, 1]

    metrics = {
        "dataset": dataset_name,
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred, zero_division=0),
        "recall": recall_score(y, y_pred, zero_division=0),
        "f1": f1_score(y, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y, y_proba),
        "classification_report": classification_report(
            y,
            y_pred,
            target_names=["humano", "ia"],
            output_dict=True,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(y, y_pred).tolist(),
    }

    return metrics


def plot_confusion_matrix(cm, output_path: str):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 5))

    ax.imshow(cm)
    ax.set_title("Matriz de Confusão - Teste")
    ax.set_xlabel("Predito")
    ax.set_ylabel("Real")

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Humano", "IA"])
    ax.set_yticklabels(["Humano", "IA"])

    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i][j]), ha="center", va="center")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_artifacts(model, vectorizer, metrics: dict, config: dict):
    model_path = Path(config["artifacts"]["model_path"])
    vectorizer_path = Path(config["artifacts"]["vectorizer_path"])
    metrics_path = Path(config["artifacts"]["metrics_path"])

    model_path.parent.mkdir(parents=True, exist_ok=True)
    vectorizer_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    with open(metrics_path, "w", encoding="utf-8") as file:
        json.dump(metrics, file, ensure_ascii=False, indent=4)


def main(config_path: str):
    config = load_config(config_path)

    text_column = config["dataset"]["text_column"]
    label_column = config["dataset"]["label_column"]

    print("Carregando e limpando dataset...")
    df = load_and_clean_dataset(config)

    print("\nQuantidade de registros após limpeza:")
    print(len(df))

    print("\nDistribuição das classes:")
    print(df[label_column].value_counts())

    print("\nSeparando treino, validação e teste...")
    train_df, val_df, test_df = split_dataset(df, config)

    save_splits(train_df, val_df, test_df, config)

    X_train_text = train_df[text_column]
    y_train = train_df[label_column]

    X_val_text = val_df[text_column]
    y_val = val_df[label_column]

    X_test_text = test_df[text_column]
    y_test = test_df[label_column]

    print("\nCriando vetorizador TF-IDF...")
    vectorizer = build_vectorizer(config)

    X_train = vectorizer.fit_transform(X_train_text)
    X_val = vectorizer.transform(X_val_text)
    X_test = vectorizer.transform(X_test_text)

    print("\nTreinando modelo...")
    model = build_model(config)
    model.fit(X_train, y_train)

    print("\nAvaliando modelo...")
    train_metrics = evaluate_model(model, X_train, y_train, "train")
    val_metrics = evaluate_model(model, X_val, y_val, "validation")
    test_metrics = evaluate_model(model, X_test, y_test, "test")

    all_metrics = {
        "train": train_metrics,
        "validation": val_metrics,
        "test": test_metrics,
        "dataset_size": {
            "total": len(df),
            "train": len(train_df),
            "validation": len(val_df),
            "test": len(test_df),
        },
        "class_distribution": df[label_column].value_counts().to_dict(),
    }

    plot_confusion_matrix(
        test_metrics["confusion_matrix"],
        config["artifacts"]["confusion_matrix_path"],
    )

    save_artifacts(model, vectorizer, all_metrics, config)

    print("\nTreinamento finalizado.")

    print("\nMétricas no TESTE:")
    print(f"Accuracy:  {test_metrics['accuracy']:.4f}")
    print(f"Precision: {test_metrics['precision']:.4f}")
    print(f"Recall:    {test_metrics['recall']:.4f}")
    print(f"F1-score:  {test_metrics['f1']:.4f}")
    print(f"ROC-AUC:   {test_metrics['roc_auc']:.4f}")

    print("\nArquivos gerados:")
    print(config["artifacts"]["model_path"])
    print(config["artifacts"]["vectorizer_path"])
    print(config["artifacts"]["metrics_path"])
    print(config["artifacts"]["confusion_matrix_path"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        default="configs/text_baseline.yaml",
        help="Caminho do arquivo de configuração YAML.",
    )

    args = parser.parse_args()

    main(args.config)