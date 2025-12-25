import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import json
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def transform_weather():
    # Carregar variáveis do .env
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        logger.error("DATABASE_URL não encontrada no arquivo .env")
        return
    
    engine = create_engine(database_url)

    logger.info("Iniciando transformação dos dados climáticos")

    # Ler dados da tabela weather_raw
    query = "SELECT regiao, data, raw_data FROM weather_raw"
    df_raw = pd.read_sql(query, engine)

    if df_raw.empty:
        logger.warning("Tabela weather_raw está vazia")
        return

    all_weather_data = []

    for _, row in df_raw.iterrows():
        raw_data = json.loads(row['raw_data'])

        all_weather_data.append({
            'regiao': row['regiao'],
            'data': row['data'],
            'temperatura_maxima': raw_data.get('temperature_2m_max'),
            'temperatura_minima': raw_data.get('temperature_2m_min'),
            'precipitacao_total': raw_data.get('precipitation_sum')
        })

    df = pd.DataFrame(all_weather_data)

    # Tratamentos
    df['data'] = pd.to_datetime(df['data'])
    df['temperatura_maxima'] = pd.to_numeric(df['temperatura_maxima'], errors='coerce')
    df['temperatura_minima'] = pd.to_numeric(df['temperatura_minima'], errors='coerce')
    df['precipitacao_total'] = pd.to_numeric(df['precipitacao_total'], errors='coerce')

    df = df.dropna()

    # Feature engineering
    df['amplitude_termica'] = df['temperatura_maxima'] - df['temperatura_minima']

    if df.empty:
        logger.warning("Nenhum dado válido após transformação")
        return

    # Batch UPSERT
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO weather_daily (
                regiao,
                data,
                temperatura_maxima,
                temperatura_minima,
                precipitacao_total,
                amplitude_termica
            )
            VALUES (
                :regiao,
                :data,
                :temperatura_maxima,
                :temperatura_minima,
                :precipitacao_total,
                :amplitude_termica
            )
            ON DUPLICATE KEY UPDATE
                temperatura_maxima = VALUES(temperatura_maxima),
                temperatura_minima = VALUES(temperatura_minima),
                precipitacao_total = VALUES(precipitacao_total),
                amplitude_termica = VALUES(amplitude_termica)
        """), df.to_dict(orient='records'))

    logger.info("Transformação e carga concluídas com sucesso")

if __name__ == "__main__":
    transform_weather()
