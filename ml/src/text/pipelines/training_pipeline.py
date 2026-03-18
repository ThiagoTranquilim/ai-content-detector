from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from src.common.config import load_yaml_config
from src.common.paths import ensure_directories
from src.common.seed import set_seed
from src.text.data.clean import clean_text_dataframe
from src.text.data.load import load_text_dataset
from src.text.data.split import split_text_dataset
from src.text.evaluation.confusion_matrix import save_confusion_matrix_figure
from src.text.evaluation.evaluate import evaluate_predictions, save_metrics
from src.text.features.tfidf import fit_transform_tfidf
from src.text.models.train_sklearn import predict_with_model, train_logistic_regression


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Treina baseline textual TF-IDF + Logistic Regression")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/text_baseline.yaml",
        help="Caminho do arquivo YAML de configuração.",
    )
    return parser.parse_args()


def save_splits(
    train_df: pd.DataFrame,
    val_df: pd.DataFrame,
    test_df: pd.DataFrame,
    config: dict,
) -> None:
    train_path = Path(config["artifacts"]["train_split_path"])
    val_path = Path(config["artifacts"]["val_split_path"])
    test_path = Path(config["artifacts"]["test_split_path"])

    for path in [train_path, val_path, test_path]:
        path.parent.mkdir(parents=True, exist_ok=True)

    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)


def main() -> None:
    args = parse_args()
    config = load_yaml_config(args.config)

    ensure_directories()
    set_seed(config["seed"])

    df = load_text_dataset(
        csv_path=config["data"]["input_csv"],
        text_column=config["data"]["text_column"],
        label_column=config["data"]["label_column"],
    )

    df = clean_text_dataframe(
        df=df,
        text_column=config["data"]["text_column"],
        label_column=config["data"]["label_column"],
        min_text_length=config["data"]["min_text_length"],
        drop_duplicates=config["data"]["drop_duplicates"],
    )

    train_df, val_df, test_df = split_text_dataset(
        df=df,
        label_column=config["data"]["label_column"],
        train_size=config["split"]["train_size"],
        val_size=config["split"]["val_size"],
        test_size=config["split"]["test_size"],
        seed=config["seed"],
        stratify=config["split"]["stratify"],
    )

    save_splits(train_df, val_df, test_df, config)

    text_col = config["data"]["text_column"]
    label_col = config["data"]["label_column"]

    vectorizer, x_train, x_val, x_test = fit_transform_tfidf(
        train_texts=train_df[text_col].tolist(),
        val_texts=val_df[text_col].tolist(),
        test_texts=test_df[text_col].tolist(),
        params=config["features"]["params"],
    )

    model_type = config["model"]["type"]
    if model_type != "logistic_regression":
        raise ValueError(f"Modelo não suportado neste MVP: {model_type}")

    model_params = dict(config["model"]["params"])
    model_params.setdefault("random_state", config["seed"])
    model = train_logistic_regression(
        x_train=x_train,
        y_train=train_df[label_col].to_numpy(),
        params=model_params,
    )

    y_val_pred, y_val_proba = predict_with_model(model, x_val)
    val_metrics = evaluate_predictions(
        y_true=val_df[label_col].to_numpy(),
        y_pred=y_val_pred,
        y_proba=y_val_proba,
    )

    y_test_pred, y_test_proba = predict_with_model(model, x_test)
    test_metrics = evaluate_predictions(
        y_true=test_df[label_col].to_numpy(),
        y_pred=y_test_pred,
        y_proba=y_test_proba,
    )

    metrics_payload = {
        "project_name": config["project_name"],
        "seed": config["seed"],
        "dataset_rows_after_cleaning": int(len(df)),
        "split_sizes": {
            "train": int(len(train_df)),
            "val": int(len(val_df)),
            "test": int(len(test_df)),
        },
        "validation": val_metrics,
        "test": test_metrics,
    }

    model_path = Path(config["artifacts"]["model_path"])
    vectorizer_path = Path(config["artifacts"]["vectorizer_path"])
    model_path.parent.mkdir(parents=True, exist_ok=True)
    vectorizer_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    save_metrics(metrics_payload, config["artifacts"]["metrics_path"])
    save_confusion_matrix_figure(
        y_true=test_df[label_col].to_numpy(),
        y_pred=y_test_pred,
        output_path=config["artifacts"]["confusion_matrix_path"],
    )

    print("Treinamento concluído com sucesso.")
    print(f"Modelo salvo em: {model_path}")
    print(f"Vetorizador salvo em: {vectorizer_path}")
    print(f"Métricas salvas em: {config['artifacts']['metrics_path']}")


if __name__ == "__main__":
    main()
