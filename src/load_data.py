from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent/ 'config' / '.env'   
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
data_base = os.getenv('data_base')
host = os.getenv('host', 'host.docker.internal')
port = os.getenv('port', '5432')

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{data_base}"
    )

engine = get_engine()

def load_weather_data(df: pd.DataFrame, table_name: str):
    df.to_sql(
        name = table_name,
        con = engine,
        if_exists = 'append',
        index = False
    )
    logging.info(f"Dados carregados com sucesso na tabela {table_name} do banco de dados {data_base}")

    with engine.connect() as conn:
        total = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
    logging.info(f"Total de registros na tabela {table_name}: {total}\n")