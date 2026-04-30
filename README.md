# Agentic Supply Chain Forecast API

Production-ready multi-agent forecasting system using LangGraph + FastAPI.

## Features
- Agent pipeline (forecast + decision)
- REST API + CSV upload
- SQLite persistence
- Dockerized

## Run

```bash
docker-compose up --build
## Generate Large Dataset

Instead of storing large CSV files, generate them:

```bash
python data/generate_data.py
