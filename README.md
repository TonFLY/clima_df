# Brasilia Weather Pipeline

This project extracts weather data for Brasilia, transforms it, and loads it into a MySQL database.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Configure settings in `config/settings.py`
3. Run the SQL script to create tables: `mysql -u username -p < sql/create_tables.sql`
4. Run the pipeline: `python ingestion/extract_weather.py` then `python transform/transform_weather.py` then `python load/load_mysql.py`
5. Schedule with cron: `crontab scheduler/cron.txt`

## Usage

- Ingestion: Fetches weather data from OpenWeatherMap API.
- Transform: Cleans and structures the data.
- Load: Inserts data into MySQL.

## Troubleshooting

- Ensure API key is set in settings.py.
- Check MySQL connection details.