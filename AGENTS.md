# Codex Agent Instructions

## Overview
This repository contains a FastAPI application that receives webhooks from the 42 intranet and sends formatted messages to a Telegram group. The project uses Python 3.12+, uv for dependency management, and follows modern type-hinted asynchronous design.

## Development Conventions
- **Python version**: 3.12 or higher. Use type hints everywhere.
- **Formatting**: Run `uv run black app/` and `uv run isort app/` on modified files before committing. The line length is 120 characters.
- **Linting**: Ensure `uv run ruff check app/` passes.
- **Type checking**: Ensure `uv run mypy app/` passes.
- **Commit style**: Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) (e.g. `feat:`, `fix:`, `docs:`).
- **Structure**: Keep code organized under the existing `app/` modules (`health`, `webhooks`, `services`). Use `APIRouter` for new endpoints and Pydantic models for requests and responses.
- **Async I/O**: Prefer asynchronous functions for operations that might block.

## Testing
Run the following checks before every commit:
```bash
uv run ruff check app/
uv run mypy app/
```
If these commands fail due to environment issues, mention it in the PR description.

## Documentation
Keep `README.md` up to date when adding new features or commands. Write docstrings for any new public functions or classes.

