FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# get packages
COPY . /app
WORKDIR /app
RUN uv sync --no-cache

CMD [ "/app/.venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]

