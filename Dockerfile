FROM python:3.13-slim AS base

# get packages
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

#install opentelemetry packages
RUN pip install opentelemetry-distro \
	opentelemetry-exporter-otlp

RUN opentelemetry-bootstrap -a install

# Add the application
COPY . .
EXPOSE 8000

ENTRYPOINT [ "opentelemetry-instrument", "fastapi", "run", "app.py"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "main.py"]
