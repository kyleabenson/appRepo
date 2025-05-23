Simple app for demostrating trace on Google Cloud
ENV Variables that Need to be set:
OTEL_SERVICE_NAME  
OTEL_TRACES_EXPORTER  
OTEL_METRICS_EXPORTER  
OTEL_EXPORTER_OTLP_ENDPOINT  

For usage in Cloud Run see the following docs for sidecar deployment, and declaring env variables there
https://cloud.google.com/stackdriver/docs/instrumentation/opentelemetry-collector-cloud-run#deploy-collector
