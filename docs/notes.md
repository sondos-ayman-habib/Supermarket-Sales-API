# Technical Notes — OS Lab Assignment #2

## 1. Biggest Docker Problem & Solution
- **Problem:** When verifying Python syntax inside the container using `compileall`, a `SyntaxError` and `IndentationError` occurred at line 1 of `src/analytics.py` due to stray PowerShell characters (`@'`) introduced during file creation.
- **Solution:** Cleaned up `src/analytics.py` to fix indentation and remove stray characters, rebuilt the image via `docker compose build`, and verified all modules with `python -m compileall -q /app/src` before running the service.

## 2. Most Important Git/GitHub Lesson Learned
- **Lesson:** Separating work into atomic, conventional commits (`feat:`, `docker:`, `chore:`, `ci:`) and developing advanced features on a dedicated branch (`feature/api-compose-ci`) before merging via a Pull Request keeps project history clean and enables automated GitHub Actions verification.
