supply-chain-agent/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI entry
│   ├── api.py               # Routes
│   ├── graph.py             # LangGraph pipeline
│   ├── nodes.py             # Agents
│   ├── db.py                # SQLite DB
│   ├── models.py            # State + schemas
│   ├── services.py          # Business logic
│   └── utils.py             # CSV loader
│
├── data/sample.csv
├── tests/test_api.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md