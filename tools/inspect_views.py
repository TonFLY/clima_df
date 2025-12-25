from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()
db = os.getenv('DATABASE_URL')
if not db:
    print('DATABASE_URL not set')
    raise SystemExit(1)
engine = create_engine(db)

views = ['weather_db.vw_weather_base', 'weather_daily']
for v in views:
    try:
        df = pd.read_sql(text(f'SELECT * FROM {v} LIMIT 1'), engine)
        print('VIEW:', v)
        print('COLUMNS:', df.columns.tolist())
        print('ROW:', df.head(1).to_dict(orient='records'))
    except Exception as e:
        print('ERROR reading', v, e)
