FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# get packages
COPY . /app
WORKDIR /app

RUN uv sync --frozen --no-cache
RUN uv run opentelemetry-bootstrap -a requirements | uv pip install --requirement -


CMD [ "/app/.venv/bin/opentelemetry-instrument","/app/.venv/bin/fastapi", "run", "main.py"]