 # Supermarket-Sales-API

A Python backend API that analyzes supermarket sales data from Kaggle. Built with **FastAPI**, containerized with **Docker**, and verified with **pytest** and **GitHub Actions CI**.

## Features

- FastAPI endpoints for sales analytics and a `/health` check
- Interactive API documentation (Swagger UI) at `/docs`
- Container health monitoring through the `/health` endpoint
- Docker Compose for one-command startup
- Unit tests with pytest
- GitHub Actions workflow that runs the tests on every push and pull request
- Makefile shortcuts for build, run, and test

## Project Structure

```
Supermarket-Sales-API/
├── src/                  # API source code
├── docs/                 # Project documentation
├── .github/workflows/    # GitHub Actions CI pipeline
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── .dockerignore
└── .gitignore
```

## Requirements

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- (Optional, for running without Docker) Python 3.12

## Quick Start

Clone the repository:

```bash
git clone https://github.com/sondos-ayman-habib/Supermarket-Sales-API.git
cd Supermarket-Sales-API
```

### Option 1: Docker Compose

```bash
docker compose up --build
```

### Option 2: Plain Docker

```bash
docker build -t supermarket-sales-api .
docker run -p 8000:8000 supermarket-sales-api
```

Once the container is running, the API is available at:

- API root: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## API Endpoints

| Method | Endpoint                 | Description                                                      |
|--------|--------------------------|------------------------------------------------------------------|
| GET    | `/health`                | Service health check                                             |
| GET    | `/summary`               | Overall summary statistics of the sales dataset                  |
| GET    | `/sales/by-branch`       | Sales totals grouped by branch                                   |
| GET    | `/sales/top-rated`       | Average customer rating per product line                         |
| GET    | `/payments`              | Number of transactions per payment method                        |
| GET    | `/pivot`                 | Pivot table of the sales data                                    |
| GET    | `/report`                | Download the full analysis as an Excel report (`.xlsx`)          |
| POST   | `/transactions/validate` | Validate a transaction (`base`, `discounted`, or `taxed`) and return its total |

Example request for `POST /transactions/validate`:

```json
{
  "product_line": "Food and beverages",
  "unit_price": 12.5,
  "quantity": 4,
  "rating": 8.0,
  "kind": "discounted",
  "rate": 0.1
}
```

Invalid transactions return HTTP `422` with an error message. Full, interactive documentation for every endpoint is available at `/docs` while the API is running.

## Configuration

| Variable    | Default                           | Description                    |
|-------------|-----------------------------------|--------------------------------|
| `DATA_PATH` | `src/data/SuperMarket Analysis.csv` | Path to the sales dataset CSV |

## Running Tests

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

Or simply:

```bash
make test
```

## Makefile Commands

| Command      | Description                                                        |
|--------------|--------------------------------------------------------------------|
| `make build` | Build the Docker image (`supermarket-sales-api`)                   |
| `make run`   | Run the container in the background on port 8000                   |
| `make stop`  | Stop and remove the container                                      |
| `make logs`  | Follow the container logs                                          |
| `make test`  | Install dev dependencies and run the pytest suite                  |
| `make clean` | Stop the container and remove the Docker image                     |

## Continuous Integration

A GitHub Actions workflow (`.github/workflows/`) runs automatically on every push and pull request to `main`. It has two jobs:

1. **test**: installs the dependencies and runs the pytest suite on Python 3.12.
2. **docker**: builds the Docker image, starts the container, and checks that `/health` responds. This job runs only if the tests pass.

## Dataset

Sales data comes from the [Supermarket Sales Dataset](https://www.kaggle.com/datasets/faresashraf1001/supermarket-sales) on Kaggle, by Fares Ashraf (Apache 2.0 license).

## Author

Sondos Ayman Habib
