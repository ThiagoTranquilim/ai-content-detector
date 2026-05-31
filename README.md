# VerificAI - Detector de Conteudo Gerado por IA

VerificAI e um projeto academico desenvolvido para analisar textos e indicar, de forma probabilistica, se o conteudo foi escrito por uma pessoa ou gerado por inteligencia artificial.

O sistema combina uma interface web simples, uma API em FastAPI e um modelo de machine learning treinado com TF-IDF e Logistic Regression.

## Funcionalidades

- Analise de textos via interface web.
- Classificacao entre `humano` e `ia`.
- Retorno de score probabilistico.
- Indicacao de nivel de confianca: `baixo`, `medio` ou `alto`.
- API REST para integracao com outros sistemas.
- Pipeline de treino e inferencia do modelo textual.

## Tecnologias utilizadas

**Frontend**

- HTML5
- CSS3
- JavaScript

**Backend**

- Python
- FastAPI
- Pydantic
- Uvicorn

**Machine Learning**

- scikit-learn
- TfidfVectorizer
- Logistic Regression
- pandas
- numpy
- joblib
- matplotlib
- PyYAML
- pytest

## Como o sistema funciona

1. O usuario digita ou cola um texto na interface web.
2. O frontend envia o texto para a API em `POST /analises/texto`.
3. O backend valida a entrada e aciona o servico de inferencia.
4. O texto e normalizado e convertido em vetores TF-IDF.
5. O modelo treinado calcula a probabilidade de o texto ter sido gerado por IA.
6. A API retorna a classe prevista, o score e o nivel de confianca.

Exemplo de resposta:

```json
{
  "predicted_class": "ia",
  "score": 0.94,
  "confidence_level": "alto"
}
```

## Estrutura do projeto

```text
ai-content-detector/
|-- backend/
|   |-- app/
|   |   |-- core/
|   |   |-- routers/
|   |   |-- schemas/
|   |   |-- services/
|   |   `-- main.py
|   `-- requirements.txt
|-- frontend/
|   |-- css/
|   |-- js/
|   `-- index.html
|-- front/
|   `-- versao antiga do frontend
`-- ml/
    |-- artifacts/
    |-- configs/
    |-- src/
    |-- tests/
    |-- README.md
    `-- requirements.txt
```

## Requisitos

- Python 3.10 ou superior
- Navegador web moderno
- pip

## Instalacao

Na raiz do projeto, crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias do backend e do modulo de machine learning:

```powershell
pip install -r backend/requirements.txt
pip install -r ml/requirements.txt
```

## Como executar o backend

A partir da raiz do projeto:

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Depois de iniciar, a API ficara disponivel em:

```text
http://localhost:8000
```

A documentacao interativa da API pode ser acessada em:

```text
http://localhost:8000/docs
```

## Como executar o frontend

Com o backend rodando, abra outro terminal e execute:

```powershell
cd frontend
python -m http.server 5500
```

Depois acesse:

```text
http://localhost:5500
```

## Endpoint principal

### Analisar texto

```http
POST /analises/texto
Content-Type: application/json
```

Corpo da requisicao:

```json
{
  "text": "Texto que sera analisado pelo sistema."
}
```

Resposta:

```json
{
  "predicted_class": "humano",
  "score": 0.87,
  "confidence_level": "alto"
}
```

## Configuracoes por variavel de ambiente

O backend aceita algumas configuracoes opcionais:

| Variavel | Descricao | Valor padrao |
| --- | --- | --- |
| `TEXT_MODEL_PATH` | Caminho do modelo treinado | `ml/artifacts/models/text_baseline.joblib` |
| `VECTORIZER_PATH` | Caminho do vetorizador TF-IDF | `ml/artifacts/vectorizers/tfidf_vectorizer.joblib` |
| `IA_THRESHOLD` | Limite minimo para classificar como IA | `0.93` |
| `USE_MOCK_INFERENCE` | Usa uma inferencia simulada | `false` |

## Treinamento do modelo

O dataset original nao esta incluido no repositorio. Para treinar novamente, adicione um CSV em:

```text
ml/data/raw/text_dataset.csv
```

O arquivo deve conter as colunas:

- `text`: texto analisado
- `generated`: classe do texto, sendo `0` para humano e `1` para IA

Execute o treino dentro da pasta `ml`:

```powershell
cd ml
python -m src.text.pipelines.training_pipeline --config configs/text_baseline.yaml
```

Ao final, o pipeline gera os artefatos em:

```text
ml/artifacts/models/text_baseline.joblib
ml/artifacts/vectorizers/tfidf_vectorizer.joblib
ml/artifacts/reports/text_metrics.json
ml/artifacts/reports/text_confusion_matrix.png
```

## Testes

Para executar os testes do modulo de machine learning:

```powershell
cd ml
pytest -q
```

## Observacoes importantes

- O sistema apresenta uma estimativa probabilistica, nao uma prova definitiva de autoria.
- O desempenho do modelo depende diretamente da qualidade e atualizacao do dataset usado no treinamento.
- Textos muito curtos, muito tecnicos ou fora do dominio do dataset podem gerar classificacoes menos confiaveis.

## Status do projeto

Projeto finalizado como entrega academica, com backend, frontend e modelo textual integrados para deteccao de conteudo gerado por IA.
