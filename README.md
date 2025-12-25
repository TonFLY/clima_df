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

## CI/CD (GitHub Actions)

This repository uses GitHub Actions for CI checks and a remote-build deploy via SSH.

- Required repository secrets (add in GitHub Settings → Secrets):
	- `DEPLOY_HOST` — IP or hostname of the server
	- `DEPLOY_USER` — SSH user for deploy
	- `DEPLOY_KEY` — private SSH key (PEM format) for `DEPLOY_USER`
	- `DEPLOY_PORT` — optional SSH port (default 22)
	- `DEPLOY_PATH` — path on remote where repo will be cloned and `docker-compose.deploy.yml` lives

- Server prerequisites:
	- `git`, `docker`, and `docker-compose` installed
	- sufficient disk space and permissions for Docker
	- optional: `curl` for remote healthchecks

- CI behavior:
	- `ci-build-push.yml` runs Python syntax checks and builds the Docker images on the runner for verification (it does not push images to a registry).

- CD behavior:
	- `cd-deploy-ssh.yml` will SSH into `DEPLOY_HOST`, pull or clone the repository into `DEPLOY_PATH`, build images using `docker-compose.deploy.yml`, and start services. It runs a basic HTTP healthcheck against `http://localhost:8501`.

If you want the deploy to use a private registry instead, revert `docker-compose.deploy.yml` to reference `image:` and add Docker registry secrets.