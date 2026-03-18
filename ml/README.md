# ML Module - AI vs Human Content Detector

MVP inicial do módulo de machine learning para classificação binária de texto:
- `0 = humano`
- `1 = IA`

Este pacote entrega um baseline textual real e executável com:
- carregamento de dataset CSV
- limpeza de texto
- split estratificado em treino/val/teste
- vetorização TF-IDF
- treinamento com Logistic Regression
- avaliação com accuracy, precision, recall, F1 e ROC-AUC
- geração de matriz de confusão
- persistência de modelo e vetorizador
- pipeline de inferência

## Estrutura

```text
ml/
├── README.md
├── requirements.txt
├── configs/
│   └── text_baseline.yaml
├── data/
│   ├── raw/
│   └── splits/
├── artifacts/
│   ├── models/
│   ├── vectorizers/
│   └── reports/
├── src/
│   ├── common/
│   └── text/
└── tests/
```

## Formato esperado do dataset

Arquivo CSV com pelo menos duas colunas:

- `text`: conteúdo textual
- `label`: classe binária
  - `0` = humano
  - `1` = IA

Exemplo:

```csv
text,label
"Este texto foi escrito por uma pessoa.",0
"Este conteúdo foi gerado por um modelo de linguagem.",1
```

## Instalação

Crie ambiente virtual e instale dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Como rodar treino

1. Coloque seu dataset em `data/raw/text_dataset.csv`
2. Execute:

```bash
python -m src.text.pipelines.training_pipeline --config configs/text_baseline.yaml
```

Ao final, serão gerados:
- `artifacts/models/text_baseline.joblib`
- `artifacts/vectorizers/tfidf_vectorizer.joblib`
- `artifacts/reports/text_metrics.json`
- `artifacts/reports/text_confusion_matrix.png`
- `data/splits/train.csv`
- `data/splits/val.csv`
- `data/splits/test.csv`

## Como rodar inferência

```bash
python -m src.text.pipelines.inference_pipeline --text "Exemplo de texto a ser classificado."
```

Saída esperada:
- rótulo previsto
- probabilidade de IA
- probabilidade de humano
- score de confiança

## Como rodar testes

```bash
pytest -q
```

## Decisões do MVP

### Modelo
Baseline textual com:
- `TfidfVectorizer`
- `LogisticRegression`

### Motivos
- rápido para implementar
- barato para treinar
- fácil de depurar
- forte baseline para comparar com transformers no futuro

## Cuidados importantes

### Overfitting
Não usar desempenho de treino como evidência principal. Sempre avaliar em validação e teste.

### Data leakage
O TF-IDF deve ser ajustado somente no conjunto de treino.

### Drift
O padrão de textos gerados por IA muda com o tempo. Re-treino e monitoramento serão necessários.

### Viés
Evite datasets em que texto humano e texto de IA diferem por tema, idioma, tamanho ou fonte de coleta.

### Desbalanceamento
Monitore a proporção das classes. O código usa split estratificado e pode usar `class_weight="balanced"`.

## Próximos passos recomendados

### MVP evoluído
- SVM linear
- embeddings semânticos
- calibrar threshold
- análise por domínio e tamanho do texto
- FastAPI consumindo o pipeline textual

### Versão avançada
- transformer para texto
- detector multimodal
- registro de experimentos
- monitoramento de drift
- explainability básica

## Observação
Este sistema produz uma **probabilidade estimada**, não uma prova definitiva de autoria humana ou por IA.
