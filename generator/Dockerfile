FROM locustio/locust
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# get packages
COPY . /locust
WORKDIR /locust
ENV PATH=/root/.local/bin:$PATH

RUN uv sync --frozen --no-cache
CMD ["uvx", "locust", "-f", "locustfile.py", "--headless", "--users" ,"10", "--spawn-rate", "2"]