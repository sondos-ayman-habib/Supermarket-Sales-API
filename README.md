# Supermarket-Sales-API

A Python backend API that analyzes supermarket sales data from Kaggle. Built with **FastAPI**, containerized with **Docker**, deployed on **GitHub Codespaces**, and verified with **pytest** and **GitHub Actions CI**.

## Features

- FastAPI endpoints for sales analytics and a `/health` check
- Interactive API documentation (Swagger UI) at `/docs`
- Multi-stage Docker build for a smaller, cleaner image
- Docker Compose for one-command startup, with a built-in health check on `/health`
- Unit tests with pytest
- GitHub Actions workflow that runs the tests on every push and pull request
- Makefile shortcuts for build, run, and test

## Production URL

The API is deployed on **GitHub Codespaces** (Docker container, port 8000, public):

- Swagger UI: https://improved-space-memory-4q7r446rx4gp39rg-8000.app.github.dev/docs
- Health check: https://improved-space-memory-4q7r446rx4gp39rg-8000.app.github.dev/health

> **Note:** Codespaces is not a permanent server. The URL works only while the
> Codespace is running, and it stops automatically after a period of inactivity. If a
> new Codespace is created with a different name, update the URL above accordingly.

## Tech Stack

- **Language:** Python 3.12
- **Framework:** FastAPI (served with Uvicorn), Pydantic
- **Data analysis:** pandas, NumPy
- **Excel report export:** openpyxl
- **Containerization:** Docker (multi-stage build), Docker Compose
- **Testing:** pytest
- **CI:** GitHub Actions
- **Automation:** Makefile
- **Deployment:** GitHub Codespaces

## Project Structure

```
Supermarket-Sales-API/
├── src/                      # API source code and dataset
│   ├── main.py               # FastAPI app and endpoints
│   ├── analytics.py          # sales analysis functions
│   ├── models.py             # transaction classes and validation
│   └── data/
│       └── SuperMarket Analysis.csv
├── tests/                    # pytest test suite
│   ├── conftest.py
│   ├── test_analytics.py
│   ├── test_api.py
│   └── test_models.py
├── docs/
│   ├── screenshots/          # assignment screenshots
│   └── notes.md              # technical notes
├── .github/workflows/        # GitHub Actions CI pipeline
├── Dockerfile                # multi-stage build
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── requirements-dev.txt
├── LICENSE.txt
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
docker run -d --name supermarket-sales-api -p 8000:8000 supermarket-sales-api
```

Both options use port 8000, so run only one at a time. To stop the Compose setup, run `docker compose down`.

Once the container is running, the API is available at:

- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## How to Test It

After the container is running:

1. Open http://localhost:8000/docs in your browser.
2. Expand `GET /health`, click **Try it out**, then **Execute**. You should get status `200` with `{"status": "ok"}`.
3. Try `GET /summary` the same way. It returns the number of rows (1000) and statistics about the dataset.

Or from a terminal:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/summary
```

## Stop and Clean Up

Docker Compose:

```bash
docker compose down
```

Plain Docker:

```bash
docker stop supermarket-sales-api
docker rm supermarket-sales-api
```

Remove the image (optional):

```bash
docker rmi supermarket-sales-api
```

With Make, `make stop` stops and removes the container, and `make clean` also removes the image.

## Deploy on a VPS / Cloud Environment

This project was deployed on **GitHub Codespaces**, a Linux environment with Docker. On a regular Ubuntu VPS the steps are the same.

1. **Check Git and Docker** (install them if they are missing):

   ```bash
   git --version
   docker --version
   docker compose version
   ```

   On Ubuntu, install Git with `sudo apt update && sudo apt install -y git`, then install Docker with `curl -fsSL https://get.docker.com | sudo sh`.

2. **Clone the repository:**

   ```bash
   git clone https://github.com/sondos-ayman-habib/Supermarket-Sales-API.git
   cd Supermarket-Sales-API
   ```

3. **Build and run the container:**

   ```bash
   docker compose up -d --build
   docker ps
   ```

   The container should show `Up ... (healthy)`.

4. **Open port 8000.** In Codespaces, add port `8000` in the **Ports** tab and set its visibility to **Public**. On a VPS, allow port `8000` in the firewall or security group.

5. **Verify the deployment** by opening `/docs` on the public URL (see [Production URL](#production-url)) and running `GET /summary`. It should return `rows: 1000`.

6. **Stop the deployment:**

   ```bash
   docker compose down
   ```

## API Endpoints

| Method | Endpoint                 | Description                                                      |
|--------|--------------------------|------------------------------------------------------------------|
| GET    | `/health`                | Service health check                                             |
| GET    | `/summary`               | Overall summary statistics of the sales dataset                  |
| GET    | `/sales/by-branch`       | Sales totals per branch, plus the top-performing branch          |
| GET    | `/sales/top-rated`       | Average customer rating per product line, plus the top-rated one |
| GET    | `/payments`              | Number of transactions per payment method, plus the most used one |
| GET    | `/pivot`                 | Pivot table of sales totals by product line and branch           |
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

Example response (12.5 x 4 = 50, minus a 10% discount):

```json
{
  "valid": true,
  "kind": "discounted",
  "total": 45.0
}
```

Invalid transactions return HTTP `422` with an error message. Full, interactive documentation for every endpoint is available at `/docs` while the API is running.

## Configuration

- **Port:** the API listens on port `8000` inside the container and is published on port `8000` of your machine (`-p 8000:8000`). To use a different port on your machine, change the left number, for example `-p 9000:8000`.
- **Environment variables:** none are required. The optional variable below is already set in `docker-compose.yml`.

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

## Attribution

This project is based on our team's earlier project, `Supermarket-Sales-Analyzer`, a set of Python scripts that analyze the Kaggle Supermarket Sales dataset. It was restructured here as a FastAPI service and containerized with Docker for this assignment. The dataset is credited in the Dataset section above.

## License

This project is licensed under the MIT License. See [LICENSE.txt](LICENSE.txt) for details.

## Author

Sondos Ayman Habib