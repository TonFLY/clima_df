#!/bin/sh
# start-cron.sh: writes crontab and runs cron in foreground

set -e

# Write cron job: run ETL at 06:00 America/Sao_Paulo daily
cat > /etc/cron.d/etl-cron <<'CRON'
# m h  dom mon dow user  command
0 6 * * * root cd /app && /usr/local/bin/python ingestion/extract_weather.py historical > /var/log/etl_historical.log 2>&1
0 6 * * * root cd /app && /usr/local/bin/python ingestion/extract_weather.py && /usr/local/bin/python transform/transform_weather.py >> /var/log/etl.log 2>&1
CRON

chmod 0644 /etc/cron.d/etl-cron
crontab /etc/cron.d/etl-cron

# Ensure log dir
mkdir -p /var/log

echo "Starting cron..."
cron -f
