import fastapi
import time
import random 
import logging
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")
@tracer.start_as_current_span("roll_d6")
def roll_d6():
  value = random.randint(1, 6)
  if value == 6:
    logging.warning("Sleeping for 4 seconds")
    #Even more sleeping to make it look like something is wrong!
    time.sleep(4)
    
  return value

app = fastapi.FastAPI()

@app.get("/")
async def foobar():
    #We're just sleeping here to make the charts look a little more gantt like
    time.sleep(2)
    roll_d6()
    return {"message": "hello world"}

FastAPIInstrumentor.instrument_app(app)
