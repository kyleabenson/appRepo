import fastapi
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


app = fastapi.FastAPI()

@app.get("/")
async def foobar():
    return {"message": "hello world"}

FastAPIInstrumentor.instrument_app(app)
