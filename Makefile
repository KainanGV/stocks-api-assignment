# Makefile for Stocks API

# Run the FastAPI server locally
run:
	uvicorn app.main:app --reload --port 8000

# Run tests with pytest
test:
	PYTHONPATH=. pytest --disable-warnings -q

# Build the Docker image
build:
	docker build -t stocks-api .

# Run the API in Docker (ensure PostgreSQL is running)
docker-run:
	docker run --env-file .env -p 8000:8000 stocks-api

# Start PostgreSQL container with Docker Compose
db-up:
	docker compose up -d

# Stop PostgreSQL container
db-down:
	docker compose down
