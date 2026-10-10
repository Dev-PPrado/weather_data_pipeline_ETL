import requests
import json
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data(url: str) -> list:
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        # Falha a tarefa para o Airflow tentar de novo, em vez de seguir com o JSON da execução anterior
        logging.error(f"Erro na requisição: status {response.status_code}")
        response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError("A API não retornou dados")


    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    logging.info(f"Dados extraídos e salvos em {output_path}")
    return data
