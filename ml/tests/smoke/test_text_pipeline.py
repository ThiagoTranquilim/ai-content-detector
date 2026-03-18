import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import yaml


def test_training_pipeline_smoke(tmp_path):
    project_root = Path(__file__).resolve().parents[2]
    config_path = project_root / "configs" / "text_baseline.yaml"

    dataset_path = tmp_path / "text_dataset.csv"
    df = pd.DataFrame(
        {
            "text": [
                "texto humano escrito manualmente com opinião própria",
                "relato pessoal com experiência concreta e subjetiva",
                "mensagem informal curta produzida por pessoa",
                "conteúdo gerado automaticamente por modelo de linguagem",
                "resposta estruturada com padrão típico de sistema de IA",
                "texto sintético criado por inteligência artificial",
                "descrição humana espontânea com detalhes do cotidiano",
                "parágrafo produzido por um assistente virtual generativo",
                "comentário humano simples sobre rotina diária",
                "frase elaborada por um modelo generativo avançado",
            ],
            "label": [0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
        }
    )
    df.to_csv(dataset_path, index=False)

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["data"]["input_csv"] = str(dataset_path)
    config["artifacts"]["model_path"] = str(tmp_path / "text_baseline.joblib")
    config["artifacts"]["vectorizer_path"] = str(tmp_path / "tfidf_vectorizer.joblib")
    config["artifacts"]["metrics_path"] = str(tmp_path / "text_metrics.json")
    config["artifacts"]["confusion_matrix_path"] = str(tmp_path / "text_confusion_matrix.png")
    config["artifacts"]["train_split_path"] = str(tmp_path / "train.csv")
    config["artifacts"]["val_split_path"] = str(tmp_path / "val.csv")
    config["artifacts"]["test_split_path"] = str(tmp_path / "test.csv")
    config["features"]["params"]["min_df"] = 1

    test_config_path = tmp_path / "test_text_baseline.yaml"
    test_config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.text.pipelines.training_pipeline",
            "--config",
            str(test_config_path),
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (tmp_path / "text_baseline.joblib").exists()
    assert (tmp_path / "tfidf_vectorizer.joblib").exists()
    assert (tmp_path / "text_metrics.json").exists()
    assert (tmp_path / "text_confusion_matrix.png").exists()

    metrics = json.loads((tmp_path / "text_metrics.json").read_text(encoding="utf-8"))
    assert "validation" in metrics
    assert "test" in metrics
    assert "accuracy" in metrics["test"]
