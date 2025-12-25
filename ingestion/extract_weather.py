import requests
import json
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_weather(historical=False):
    # Carregar variáveis do .env
    load_dotenv()
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL não encontrada no arquivo .env")
        return
    
    engine = create_engine(database_url)
    
    # Regiões administrativas de Brasília (DF) com coordenadas aproximadas
    regions = [
        {"name": "Plano Piloto", "lat": -15.7833, "lon": -47.9167},
        {"name": "Asa Norte", "lat": -15.7633, "lon": -47.8833},
        {"name": "Asa Sul", "lat": -15.8067, "lon": -47.8833},
        {"name": "Taguatinga", "lat": -15.8333, "lon": -48.0667},
        {"name": "Ceilândia", "lat": -15.8167, "lon": -48.1167},
        {"name": "Samambaia", "lat": -15.8667, "lon": -48.0833},
        {"name": "Sobradinho", "lat": -15.65, "lon": -47.7833},
        {"name": "Planaltina", "lat": -15.6167, "lon": -47.65},
        {"name": "Gama", "lat": -16.0167, "lon": -48.0667},
        {"name": "Guará", "lat": -15.8167, "lon": -47.9833},
        {"name": "Núcleo Bandeirante", "lat": -15.8667, "lon": -47.9667},
        {"name": "Paranoá", "lat": -15.7667, "lon": -47.7833},
        {"name": "Itapoã", "lat": -15.75, "lon": -47.7667},
        {"name": "Jardim Botânico", "lat": -15.8667, "lon": -47.8},
        {"name": "Lago Sul", "lat": -15.8667, "lon": -47.8667},
        {"name": "Lago Norte", "lat": -15.7167, "lon": -47.8833},
        {"name": "Candangolândia", "lat": -15.85, "lon": -47.95},
        {"name": "Varjão", "lat": -15.7167, "lon": -47.8833},
        {"name": "SIA", "lat": -15.8, "lon": -47.9667},
        {"name": "Sudoeste", "lat": -15.7833, "lon": -47.9167},
        {"name": "Santa Maria", "lat": -16.0167, "lon": -47.9833},
        {"name": "São Sebastião", "lat": -15.9, "lon": -47.7667},
        {"name": "Recanto das Emas", "lat": -15.9167, "lon": -48.0667},
        {"name": "Riacho Fundo", "lat": -15.8833, "lon": -48.0167},
        {"name": "Riacho Fundo II", "lat": -15.9, "lon": -48.0333},
        {"name": "Estrutural", "lat": -15.7833, "lon": -47.9833},
        {"name": "Vicente Pires", "lat": -15.8, "lon": -48.0333},
        {"name": "Águas Claras", "lat": -15.8333, "lon": -48.0333},
        {"name": "Arniqueira", "lat": -15.85, "lon": -47.9667},
        {"name": "Brazlândia", "lat": -15.6667, "lon": -48.2},
        {"name": "Cruzeiro", "lat": -15.7833, "lon": -47.9333},
        {"name": "Fercal", "lat": -15.6, "lon": -47.8667},
        {"name": "Park Way", "lat": -15.9, "lon": -47.8167},
        {"name": "SCIA", "lat": -15.7833, "lon": -47.9667},
        {"name": "Sobradinho II", "lat": -15.6333, "lon": -47.8167}
    ]
    
    with engine.begin() as conn:  # Transação explícita
        for region in regions:
            try:
                if historical:
                    # API histórica para backfill
                    end_date = datetime.date.today()
                    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={region['lat']}&longitude={region['lon']}&start_date=2025-01-01&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/Sao_Paulo"
                else:
                    # API de forecast para operação normal
                    url = f"https://api.open-meteo.com/v1/forecast?latitude={region['lat']}&longitude={region['lon']}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America/Sao_Paulo"
                
                response = requests.get(url, timeout=10)
                response.raise_for_status()  # Levanta erro para status != 200
                data = response.json()
                
                # Inserir dados brutos por data (não o JSON inteiro repetido)
                daily = data['daily']
                times = daily['time']
                temp_max = daily['temperature_2m_max']
                temp_min = daily['temperature_2m_min']
                precipitation = daily['precipitation_sum']
                
                for i, date in enumerate(times):
                    raw_data = json.dumps({
                        "temperature_2m_max": temp_max[i],
                        "temperature_2m_min": temp_min[i],
                        "precipitation_sum": precipitation[i]
                    })
                    conn.execute(text("""
                        INSERT INTO weather_raw (regiao, data, raw_data)
                        VALUES (:regiao, :data, :raw_data)
                        ON DUPLICATE KEY UPDATE raw_data = VALUES(raw_data)
                    """), {
                        'regiao': region['name'],
                        'data': date,
                        'raw_data': raw_data
                    })
                logger.info(f"Dados brutos inseridos para {region['name']} - {len(times)} dias")
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro na requisição para {region['name']}: {e}")
            except Exception as e:
                logger.error(f"Erro inesperado para {region['name']}: {e}")

if __name__ == "__main__":
    import sys
    historical = len(sys.argv) > 1 and sys.argv[1] == 'historical'
    extract_weather(historical=historical)