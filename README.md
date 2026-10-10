# Pipeline ETL de dados climáticos

**Página no portfólio:** https://dev-pprado.github.io/projetos/pipeline-weather/

Pipeline que coleta o clima atual de São Paulo na API do [OpenWeatherMap](https://openweathermap.org/api) a cada hora, transforma com Pandas e carrega no PostgreSQL. A orquestração é feita pelo Apache Airflow, com todo o ambiente em Docker.

O projeto começou a partir do [tutorial da VBLUUIZA](https://www.youtube.com/watch?v=I8qPqbXQBDU) ([repositório original](https://github.com/vbluuiza/pipeline_etl_weather_data_tutorial_youtube)) e está sendo evoluído a partir dele.

## O pipeline

```mermaid
flowchart LR
  API[API OpenWeatherMap<br/>São Paulo, units=metric] --> E[extract<br/>JSON bruto]
  E --> J[(data/weather_data.json)]
  J --> T[transform<br/>Pandas]
  T --> P[(data/temp_data.parquet)]
  P --> L[load<br/>SQLAlchemy]
  L --> DB[(PostgreSQL<br/>tabela sp_weather)]
  AF[Airflow<br/>DAG weather_pipeline, a cada hora] -.orquestra.-> E
```

A DAG fica em [`dags/weather_dag.py`](dags/weather_dag.py) e as etapas em [`src/`](src).

| Etapa | Código | O que faz |
|---|---|---|
| **Extract** | [`src/extract_data.py`](src/extract_data.py) | Chama a API do OpenWeatherMap e salva a resposta em `data/weather_data.json`. Se a API falhar, a tarefa falha e o Airflow tenta de novo. |
| **Transform** | [`src/transform_data.py`](src/transform_data.py) | Achata o JSON com `json_normalize`, abre a lista `weather` em colunas próprias, remove colunas sem uso, renomeia (`main.temp` → `temperature`, `dt` → `datetime`...) e converte `datetime`, `sunrise` e `sunset` de Unix para o fuso `America/Sao_Paulo`. O resultado vai para `data/temp_data.parquet`. |
| **Load** | [`src/load_data.py`](src/load_data.py) | Lê o Parquet e faz `to_sql` em modo `append` na tabela `sp_weather`. Depois registra no log o total de linhas da tabela (`COUNT(*)`). |

### A DAG

| Configuração | Valor |
|---|---|
| `dag_id` | `weather_pipeline` |
| Agenda | `0 * * * *` (a cada hora) |
| Tarefas | `extract >> transform >> load` |
| Retries | 1, com 5 minutos de espera |
| `catchup` | `False` (não roda execuções passadas) |

Para rodar as etapas fora do Airflow (por exemplo, para depurar), `uv sync` instala as dependências locais.

### Tabela `sp_weather` (algumas colunas)

A tabela é criada pelo próprio Pandas na primeira carga, então os tipos são os inferidos por ele.

| Coluna | Tipo | Regra |
|---|---|---|
| `datetime` | timestamptz | Fuso America/Sao_Paulo |
| `city_name` | text | |
| `temperature` | double precision | °C |
| `humidity` | bigint | % |
| `weather_description` | text | |

### Decisões de engenharia

- **Uma tarefa por etapa:** extract, transform e load são tarefas separadas no Airflow, então dá para ver e reexecutar cada uma pela interface.
- **Arquivos intermediários:** as tarefas trocam dados por arquivo (JSON bruto e Parquet) em `data/`, uma pasta compartilhada entre os containers. O Parquet mantém os tipos (inclusive o fuso das datas) entre o transform e o load.
- **Histórico em append:** cada execução adiciona uma linha nova em `sp_weather`, formando uma série temporal do clima.
- **Falha explícita no extract:** um erro da API (chave inválida, limite, timeout de 30 s) derruba a tarefa em vez de seguir com o JSON da execução anterior. Assim o retry do Airflow entra em ação e o transform nunca reprocessa dado velho como se fosse novo.
- **Credenciais fora do código:** chave da API e acesso ao banco ficam em `config/.env`, que não é versionado.
- **Logs:** cada etapa usa `logging`, visível nos logs das tarefas no Airflow.

## Stack

| Parte | Tecnologias |
|---|---|
| Pipeline | Python, Requests, Pandas, Parquet, SQLAlchemy, psycopg2 |
| Orquestração | Apache Airflow 3 (CeleryExecutor, Redis) |
| Banco | PostgreSQL |
| Infraestrutura | Docker, Docker Compose, uv |

## Como rodar localmente

Pré-requisitos: Docker com Docker Compose e uma [chave de API do OpenWeatherMap](https://home.openweathermap.org/api_keys).

1. Crie `config/.env` com a chave da API e o acesso ao PostgreSQL onde os dados serão gravados. O jeito mais simples é usar o PostgreSQL do próprio compose:

   ```env
   API_KEY=sua_chave_aqui
   user=airflow
   password=airflow
   data_base=airflow
   host=postgres
   ```

   Para gravar num PostgreSQL da sua máquina, troque o usuário, a senha e o banco e remova `host` (o padrão é `host.docker.internal`). A porta pode ser alterada com `port` (padrão `5432`).

2. Crie um `.env` na raiz (o `docker-compose.yaml` exige esse arquivo):

   ```env
   AIRFLOW_UID=50000
   ```

3. Suba o ambiente:

   ```sh
   docker compose up -d
   docker compose ps     # espere os serviços ficarem healthy
   ```

4. Acesse o Airflow em http://localhost:8080 (usuário e senha `airflow`), ative a DAG `weather_pipeline` (ela começa pausada) e dispare uma execução.

Para explorar o JSON extraído, há um notebook em [`notebooks/analysis_data.ipynb`](notebooks/analysis_data.ipynb).

## Estrutura

```text
.
├── dags/
│   └── weather_dag.py        # DAG weather_pipeline
├── src/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
├── notebooks/
│   └── analysis_data.ipynb   # exploração do JSON da API
├── images/                   # pipeline_architecture.png
├── docker-compose.yaml       # Airflow, PostgreSQL de metadados e Redis
├── main.py                   # versão antiga do pipeline sem Airflow (comentada)
└── pyproject.toml
```

As pastas `config/`, `data/`, `logs/` e `plugins/` são montadas nos containers e ficam fora do Git.

## Limitações conhecidas

- **Cidade fixa:** a URL da API está na DAG com São Paulo.
- **Sem validação de schema:** uma resposta da API com formato diferente do esperado só quebra no transform.
- **Banco compartilhado:** usando `host=postgres`, a tabela `sp_weather` fica no mesmo banco de metadados do Airflow. Serve para estudo; em produção o destino seria um banco separado.
- **Sem testes automatizados.**

## Próximos passos

- [ ] Validação e qualidade dos dados
- [ ] Testes automatizados
- [ ] Carga incremental
- [ ] Arquitetura medallion (bronze, silver, gold)
- [ ] Processamento com PySpark
- [ ] Deploy em cloud
