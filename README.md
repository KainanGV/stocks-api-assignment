# Stocks API

FastAPI service that fetches stock information from Polygon.io and MarketWatch. Purchase amounts are stored in PostgreSQL. The application follows a clean architecture with a service layer, repository pattern and dependency injection.

## Features

- Retrieve open/high/low/close prices with Polygon.io
- Scrape company name, performance and competitor data from MarketWatch
- Cache responses per stock for five minutes
- Persist purchased amounts in PostgreSQL using SQLAlchemy
- Automatically apply Alembic migrations on startup
- Fully dockerized development environment

## Requirements

- Python 3.10+
- Docker and Docker Compose

## Running locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env 
export DATABASE_URL=postgresql://stocks:stocks123@localhost:5432/stocksdb
docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

You can also place these variables in a `.env` file so they are loaded automatically.

Open [http://localhost:8000/docs](http://localhost:8000/docs) to interact with the API.

## Running with Docker

The compose file builds the API image and starts both the database and the application. Migrations are executed automatically. Copy `.env.example` to `.env` and set your Polygon key so the container can fetch data.

```bash
docker-compose up --build
```

The service will be available on port `8000`.

## Running tests

```bash
TESTING=1 pytest -q
```

> The `TESTING=1` flag ensures that external dependencies like the database and APIs are **automatically mocked**, allowing unit tests to run without a real PostgreSQL or API calls.

### API Evidence

#### Example GET `/stock/aapl`
![Stock Info](assets/image.png)

```json
{
  "symbol": "aapl",
  "date": "2025-07-18",
  "status": "OK",
  "company_name": "Apple Inc.",
  "stock_values": {
    "open": 210.87,
    "high": 211.79,
    "low": 209.7045,
    "close": 211.18
  },
  "performance_data": {
    "five_days": "0.01%",
    "one_month": "5.06%",
    "three_months": "7.21%",
    "year_to_date": "-15.67%",
    "one_year": "-5.85%"
  },
  "competitors": [
    {"name": "Microsoft Corp.", "chg_percent": "-0.32%", "market_cap": "$3.8T"},
    {"name": "Alphabet Inc. Cl C", "chg_percent": "0.67%", "market_cap": "$2.23T"},
    {"name": "Alphabet Inc. Cl A", "chg_percent": "0.81%", "market_cap": "$2.23T"},
    {"name": "Amazon.com Inc.", "chg_percent": "1.01%", "market_cap": "$2.38T"},
    {"name": "Meta Platforms Inc.", "chg_percent": "0.41%", "market_cap": "$1.76T"},
    {"name": "Samsung Electronics Co. Ltd.", "chg_percent": "0.60%", "market_cap": "₩440.01T"},
    {"name": "Samsung Electronics Co. Ltd. Pfd. Series 1", "chg_percent": "-0.36%", "market_cap": "₩440.01T"},
    {"name": "Sony Group Corp.", "chg_percent": "-1.87%", "market_cap": "¥21.78T"},
    {"name": "Dell Technologies Inc.", "chg_percent": "5.94%", "market_cap": "$84.1B"},
    {"name": "HP Inc.", "chg_percent": "1.25%", "market_cap": "$23.25B"}
  ]
}
```

#### Example POST `/stock/aapl?amount=5`
![Stock Added](assets/image-1.png)

```json
{
  "message": "5 units of stock aapl were added to your stock record"
}
```

#### Tests
![alt text](assets/image-2.png)
