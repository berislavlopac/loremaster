dotenv-filename := ".env"

# List available recipes.
help:
    @just --list --unsorted

# Run unit tests.
test:
    uv run pytest tests/unit/ --spec

# Run unit tests with coverage report.
test-cov:
    uv run pytest tests/unit/ --cov --spec

# Run linting and formating checks.
lint:
    uv run deptry .
    uv run ruff format --check .
    uv run ruff check .

# Run static typing analysis.
type:
    uv run mypy --install-types --non-interactive

# Run security checks.
safety:
    uvx vulture --min-confidence 100 files_router/
    uvx radon mi --show --multi --min B files_router/
    uvx complexipy --details low files_router/

# Run all checks.
check: lint safety type

# Reformat the code using isort and ruff.
[confirm]
reformat:
    uv run ruff format .
    uv run ruff check --select I --fix .

# Serve documentation website for development purposes
docs:
    uv run mkdocs serve

# Extract current production requirements. Save to a file by appending `> requirements.txt`.
reqs:
    uv export --no-default-groups

# Run the development server locally.
serve:
    uv run uvicorn email_ingestion.api:app --host 0.0.0.0 --port 8000 --reload --log-level debug

# Build the development container.
build:
    docker build --target dev -t files-router-dev .

# Build the production container.
build-prod:
    docker build --target prod -t files-router .
