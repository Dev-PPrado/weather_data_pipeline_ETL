🌤️ Pipeline ETL — Dados Climáticos de São Paulo

Pipeline de Engenharia de Dados desenvolvido para coleta, transformação e armazenamento de dados meteorológicos da cidade de São Paulo.

O projeto utiliza Python, Apache Airflow, PostgreSQL e Docker, implementando um fluxo ETL automatizado e orquestrado.

📚 Projeto de estudo baseado nos ensinamentos e no tutorial da VBLUUIZA.

O objetivo é utilizar os conceitos apresentados no conteúdo como base de aprendizado e, posteriormente, evoluir o projeto com novas práticas e tecnologias de Engenharia de Dados.

📌 Sobre o Projeto

Este projeto foi desenvolvido como parte dos meus estudos em Engenharia de Dados, com o objetivo de colocar em prática conceitos fundamentais de construção de pipelines ETL.

O pipeline realiza as seguintes etapas:

OpenWeatherMap API
        │
        ▼
    EXTRACT
        │
        ▼
    JSON bruto
        │
        ▼
   TRANSFORM
        │
        ▼
    Parquet
        │
        ▼
      LOAD
        │
        ▼
   PostgreSQL

A execução do pipeline é realizada pelo Apache Airflow, permitindo a orquestração e o agendamento automático das etapas.

Atualmente, o pipeline está configurado para executar a cada hora.

🎯 Objetivos de Aprendizado

Este projeto tem como principais objetivos:

Desenvolver um pipeline ETL completo;
Consumir dados de uma API REST;
Trabalhar com dados JSON;
Realizar transformação e normalização de dados;
Utilizar Pandas para manipulação de dados;
Trabalhar com arquivos Parquet;
Persistir dados em PostgreSQL;
Utilizar Apache Airflow para orquestração;
Utilizar Docker e Docker Compose;
Trabalhar com variáveis de ambiente;
Desenvolver uma estrutura organizada de projeto;
Praticar conceitos fundamentais de Engenharia de Dados.
🏗️ Arquitetura

A arquitetura atual do pipeline é baseada no fluxo:

Extract → Transform → Load

┌──────────────────────┐
│ OpenWeatherMap API   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Extract        │
│   Python + Requests  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Dados Brutos      │
│        JSON          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Transform       │
│ Pandas + Normalização│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Parquet        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│        Load          │
│     PostgreSQL       │
└──────────────────────┘

O Apache Airflow é responsável por orquestrar todo o fluxo:

Extract → Transform → Load
🛠️ Tecnologias Utilizadas
Linguagens e processamento
Python
Pandas
Requests
SQLAlchemy
psycopg2
Engenharia de Dados
Apache Airflow
PostgreSQL
Parquet
ETL
API REST
Infraestrutura
Docker
Docker Compose
Redis
Desenvolvimento
UV
Jupyter Notebook
Git / GitHub
📂 Estrutura do Projeto

A estrutura principal do projeto está organizada da seguinte forma:

.
├── dags/
│   └── weather_dag.py
│
├── src/
│   ├── extract_data.py
│   ├── transform_data.py
│   └── load_data.py
│
├── data/
│   ├── weather_data.json
│   └── temp_data.parquet
│
├── notebooks/
│   └── ...
│
├── config/
│   └── .env
│
├── logs/
│
├── plugins/
│
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
├── main.py
└── README.md
🔄 Pipeline ETL
📥 1. Extract

Arquivo:

src/extract_data.py

Nesta etapa, o pipeline realiza uma requisição HTTP para a API do OpenWeatherMap.

Os dados retornados são armazenados inicialmente em formato JSON.

Entre as informações coletadas estão:

Temperatura atual;
Temperatura mínima e máxima;
Sensação térmica;
Umidade;
Pressão atmosférica;
Velocidade do vento;
Direção do vento;
Cobertura de nuvens;
Horário do nascer do sol;
Horário do pôr do sol;
Coordenadas geográficas;
Condições climáticas.
🔄 2. Transform

Arquivo:

src/transform_data.py

Nesta etapa os dados brutos são transformados em uma estrutura adequada para armazenamento e análise.

São realizadas operações como:

Leitura do JSON;
Conversão para DataFrame;
Normalização de dados aninhados;
Tratamento da coluna weather;
Remoção de informações desnecessárias;
Renomeação das colunas;
Conversão de timestamps;
Conversão para o fuso horário de São Paulo.

Exemplo:

main.temp       → temperature
main.humidity   → humidity
coord.lon       → longitude
sys.sunrise     → sunrise
sys.sunset      → sunset

Ao final dessa etapa, os dados são armazenados temporariamente em formato Parquet.

Por que Parquet?

O Parquet é utilizado como formato intermediário por ser eficiente para armazenamento e processamento de dados, além de preservar os tipos das colunas.

💾 3. Load

Arquivo:

src/load_data.py

A etapa de Load realiza a conexão com o PostgreSQL e insere os dados transformados na tabela:

sp_weather

A inserção é realizada utilizando SQLAlchemy e Pandas.

Também é realizada uma validação através da contagem dos registros armazenados no banco.

⚙️ Orquestração com Apache Airflow

Arquivo:

dags/weather_dag.py

A DAG principal do projeto é:

youtube_weather_pipeline

O fluxo possui três tarefas principais:

extract()
     ↓
transform()
     ↓
load()

A DAG está configurada para executar o pipeline automaticamente a cada hora.

0 */1 * * *

O parâmetro catchup=False evita a execução automática de períodos anteriores.

🐳 Docker

O projeto utiliza Docker para facilitar a criação do ambiente de desenvolvimento.

Os principais serviços utilizados são:

Airflow API Server;
Airflow Scheduler;
Airflow Worker;
Airflow Triggerer;
PostgreSQL;
Redis.

Isso permite reproduzir o ambiente de execução sem a necessidade de instalar manualmente todos os componentes.

🚀 Como Executar
1. Clone o projeto
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
2. Configure a API

Crie uma conta no OpenWeatherMap e obtenha uma API Key.

Depois configure as variáveis de ambiente.

Exemplo:

API_KEY=sua_chave_api

user=airflow
password=airflow
database=airflow

⚠️ Nunca envie seu arquivo .env para o GitHub.

Adicione-o ao .gitignore.

3. Inicie o ambiente Docker
docker-compose up -d

Verifique os containers:

docker-compose ps

Os serviços devem aparecer como running ou healthy.

4. Acesse o Airflow

Abra:

http://localhost:8080

Utilize as credenciais configuradas no ambiente.

Depois localize a DAG:

youtube_weather_pipeline

e execute o pipeline.

🧪 Execução Local

Também é possível executar o projeto sem utilizar o Airflow para testes locais.

Instale as dependências:

uv pip install -e .

Execute:

uv run main.py

O main.py pode ser utilizado para validar o funcionamento das etapas individualmente.

📊 Dados Armazenados

Os dados meteorológicos são armazenados na tabela:

sp_weather

O banco PostgreSQL permite posteriormente realizar consultas e análises sobre o histórico coletado.

Algumas possibilidades de análise incluem:

Evolução da temperatura;
Temperatura média por período;
Variação da umidade;
Relação entre temperatura e umidade;
Velocidade média do vento;
Condições climáticas mais frequentes;
Evolução das condições meteorológicas ao longo do tempo.
🗺️ Roadmap — Próximas Evoluções

Este projeto será utilizado como uma base prática para evoluir meus conhecimentos em Engenharia de Dados.

As próximas versões serão desenvolvidas gradualmente conforme avanço nos estudos.

✅ Etapa 1 — Pipeline ETL

Consumo de API REST

Extração dos dados

Transformação com Pandas

Armazenamento em Parquet

Carga no PostgreSQL

Orquestração com Airflow

Containerização com Docker

🔜 Etapa 2 — Qualidade e confiabilidade

Implementar validações de qualidade dos dados

Validar valores nulos

Validar tipos de dados

Validar duplicidades

Implementar tratamento de erros

Melhorar logging

Criar mecanismos de retry

Criar testes automatizados

🔜 Etapa 3 — Arquitetura de Dados

Evoluir o pipeline para uma arquitetura Medallion

Criar camada Bronze para dados brutos

Criar camada Silver para dados tratados

Criar camada Gold para dados preparados para consumo

Melhorar organização do armazenamento

Separar claramente as responsabilidades de cada camada

Arquitetura planejada:

              API
               │
               ▼
        ┌─────────────┐
        │   BRONZE    │
        │ Dados brutos│
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │   SILVER    │
        │Dados tratados│
        └──────┬──────┘
               │
               ▼
        ┌─────────────┐
        │    GOLD     │
        │Dados prontos │
        │para consumo  │
        └─────────────┘
🔜 Etapa 4 — Engenharia de Dados

Introduzir SQL de forma mais aprofundada

Melhorar modelagem dos dados

Implementar particionamento

Avaliar estratégias de indexação

Melhorar performance das consultas

Implementar incremental loading

Trabalhar com diferentes formatos de dados

Avaliar utilização de processamento distribuído

🔜 Etapa 5 — Analytics Engineering

Como parte da evolução dos estudos:

Avaliar utilização do dbt

Criar modelos SQL

Implementar testes de dados

Documentar modelos

Criar camada de transformação mais estruturada

🔜 Etapa 6 — Cloud

Posteriormente, o projeto poderá ser adaptado para um ambiente cloud:

AWS

Object Storage

Banco de dados gerenciado

Orquestração em cloud

IAM e gerenciamento de credenciais

Monitoramento

🔜 Etapa 7 — Evolução para Data & AI

Como etapa posterior da minha jornada de estudos:

Construir datasets analíticos

Realizar análises exploratórias

Feature Engineering

Aplicar Machine Learning

Criar modelos preditivos

Integrar modelos ao pipeline

Estudar MLOps

📚 Referência e Base de Estudo

Este projeto foi desenvolvido seguindo os ensinamentos apresentados pela VBLUUIZA, utilizando o tutorial como base prática para compreender a construção de um pipeline ETL com Python, Airflow, PostgreSQL e Docker.

O objetivo não é apenas reproduzir o projeto, mas utilizá-lo como ponto de partida para experimentação e evolução, adicionando gradualmente novos conceitos aprendidos durante minha formação em Engenharia de Dados.

Conteúdo utilizado como referência
📺 Tutorial no YouTube — VBLUUIZA
💻 Repositório original — VBLUUIZA
📄 Documentação complementar disponibilizada no tutorial
📈 Evolução do Projeto

A ideia deste repositório é acompanhar minha evolução prática na área de Engenharia de Dados.

Por isso, novas funcionalidades serão adicionadas conforme avanço nos estudos, transformando o projeto gradualmente de um ETL simples em uma arquitetura de dados mais completa.

ETL básico
   ↓
Qualidade de dados
   ↓
Medallion Architecture
   ↓
Testes
   ↓
Processamento distribuído
   ↓
Cloud
   ↓
Data Engineering
   ↓
Data & AI
🐛 Troubleshooting
DAG não aparece no Airflow

Verifique os logs:

docker-compose logs airflow-scheduler

Caso necessário:

docker-compose restart
Erro de conexão com PostgreSQL

Verifique:

docker-compose ps

Confirme se o container do PostgreSQL está em execução.

Erro 401 na API

Verifique:

Se a API Key foi configurada;
Se o arquivo .env está no local correto;
Se a variável API_KEY está preenchida corretamente.
🛑 Encerrando o Ambiente

Para parar os containers:

docker-compose down

Para remover os containers e volumes:

docker-compose down -v

⚠️ O comando acima pode remover os dados armazenados nos volumes.

👨‍💻 Autor

Pedro Henrique de Souza Prado

Engenheiro de Controle e Automação em transição para Engenharia de Dados, com foco em construção de pipelines, processamento de dados, Python, SQL e tecnologias de dados.

🔗 LinkedIn

💻 GitHub

📌 Observação

Este é um projeto de estudo e portfólio.

A implementação inicial foi construída com base no conteúdo educacional da VBLUUIZA, sendo posteriormente utilizada como base para novos estudos e futuras melhorias relacionadas à Engenharia de Dados.

⭐ Se este projeto for útil para seus estudos, fique à vontade para deixar uma estrela no repositório!
