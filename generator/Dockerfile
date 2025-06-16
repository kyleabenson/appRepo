FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# get packages
COPY . /locust
WORKDIR /locust
ENV PATH=/root/.local/bin:$PATH
RUN uv sync --frozen --no-cache
# RUN uv sync --frozen --no-cache
ENV PATH="/locust/.venv/bin:$PATH"
#This variable must be overwridden at runtime to actually run against the backend instance
ENV LOCUST_HOST=""
ENV LOCUST_RUN_TIME="45m"
ENV LOCUST_USERS="10"
CMD ["locust","-f", "locustfile.py", "--headless", "--exit-code-on-error" ," 0"]
