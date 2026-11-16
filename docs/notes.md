# Technical Notes — OS Lab Assignment #2

## 1. Docker & Syntax Troubleshooting
- **Problem:** While checking Python syntax inside the container using `compileall`, a `SyntaxError` and `IndentationError` appeared at the beginning of `src/analytics.py` due to stray characters (`@'`) from file creation.
- **Solution:** Cleaned up the file structure, fixed the indentation, rebuilt the image (`docker compose build`), and re-ran `python -m compileall -q /app/src` to ensure everything compiled cleanly before starting the service.

## 2. Git Workflow & Branching
- **Lesson:** Using a separate branch (`feature/api-compose-ci`) and breaking work into small, clear commits (`feat:`, `docker:`, `chore:`, `ci:`) made it much easier to track changes and collaborate cleanly without messing up the main branch.

## 3. Automated CI/CD (GitHub Actions)
- **Experience:** Setting up GitHub Actions to automatically run unit tests (`pytest`) and build the Docker image on every Pull Request gave us instant feedback and ensured that our code changes didn't break anything.

## 4. Makefile Shortcuts
- **Usage:** Adding a Makefile helped automate repetitive terminal commands (`build`, `run`, `test`), making it faster and simpler to manage the project locally.

## 5. Automated Unit Testing
- **Implementation:** Added a dedicated `tests/` directory with `pytest` covering API endpoints, data models, and analytics logic to ensure code correctness and catch bugs early.

## 6. API Structure & Data Validation
- **Implementation:** Built the backend using FastAPI and structured data models to handle supermarket sales queries and validate inputs efficiently.
