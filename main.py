import fastapi
import time
import random 
import logging

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def roll_d6():
  value = random.randint(1, 6)
  if value == 6:
    logging.warning("Sleeping for 4 seconds")
    time.sleep(4)
    
  return value

app = fastapi.FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/")
async def foobar():
    roll_d6()
    return {"message": "hello world"}

FastAPIInstrumentor.instrument_app(app)
