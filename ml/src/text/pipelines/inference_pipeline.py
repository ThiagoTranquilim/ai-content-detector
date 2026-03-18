from __future__ import annotations

import argparse
import json

from src.common.config import load_yaml_config
from src.text.models.predict import load_inference_artifacts, predict_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Executa inferência no baseline textual.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/text_baseline.yaml",
        help="Caminho do arquivo YAML de configuração.",
    )
    parser.add_argument(
        "--text",
        type=str,
        required=True,
        help="Texto bruto para classificação.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_yaml_config(args.config)

    model, vectorizer = load_inference_artifacts(
        model_path=config["artifacts"]["model_path"],
        vectorizer_path=config["artifacts"]["vectorizer_path"],
    )

    prediction = predict_text(args.text, model, vectorizer)
    print(json.dumps(prediction.__dict__, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
