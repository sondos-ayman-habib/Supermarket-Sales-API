 # Technical Notes — OS Lab Assignments #2 and #3

## Assignment 2: Docker & GitHub

### 1. Choosing the project
- **Challenge:** Selecting a project suitable for the lab that is meaningful, testable by users, and straightforward to run inside Docker, since our earlier work consisted of standalone Python analysis scripts rather than a service.
- **Solution:** Converted the analysis scripts into a FastAPI application exposing endpoints such as `/health`, `/summary`, and `/sales/by-branch`, and bundled the dataset inside the repository (`src/data/`) so building the image requires no external downloads.

### 2. Biggest Docker problems
- **Problem:** `requirements.txt` initially listed only `fastapi` and `uvicorn`, even though the application code imports `pandas`, `numpy`, and `openpyxl`. The image would have built without `pip install` errors, but the container would have failed at startup with `ModuleNotFoundError`.
- **Solution:** Added `pandas`, `numpy`, and `openpyxl` to `requirements.txt` while preserving the version constraints for `fastapi` and `uvicorn`, then rebuilt the image with `docker compose build`.
- **Problem:** Running `python -m compileall` inside the container reported a `SyntaxError` and an `IndentationError` in `src/analytics.py` caused by stray PowerShell characters (`@'`) saved into the file.
- **Solution:** Removed the stray characters from `src/analytics.py`, rebuilt the image with `docker compose build`, and re-ran `python -m compileall` until it completed cleanly with zero errors.

### 3. Most important Git/GitHub lesson
- Developing on a feature branch (`feature/api-compose-ci`) and merging via a Pull Request with small, prefixed commits (`feat:`, `docker:`, `docs:`) kept `main` clean and made the commit history easy to trace. GitHub Actions ran checks on each push, helping catch issues early.

## Assignment 3: Deployment to a VPS

**Provider and environment:** GitHub Codespaces (Linux, Docker).

### Challenges and how I solved them
- **Challenge:** Opening the forwarded public URL in the browser returned `HTTP 401`.
- **Solution:** Port `8000` was still set to `Private` in the **Ports** tab. Changing its visibility to `Public` allowed access to the API (including `/docs`) without authentication prompts.
- **Challenge:** After stopping and restarting the Codespace, `docker compose up -d` failed with `failed to extract layer ... content digest ... not found`.
- **Solution:** The local Docker image/build cache was corrupted. Removed the affected image and build cache, rebuilt cleanly with `docker compose build --no-cache`, and started the container again.
- **Challenge:** Missed taking a screenshot of `git clone` before uploading screenshots to GitHub, while the workspace already contained the cloned repository.
- **Solution:** Cloned the repository into a temporary directory (`/tmp`), captured the screenshot, and deleted `/tmp` afterward without disturbing the active project workspace.