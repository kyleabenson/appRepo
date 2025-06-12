from time import sleep
import random
import logging
from fastapi import FastAPI, Response, status
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from sqlmodel import Session, select
from .database import Song, engine, create_db_and_tables
from contextlib import asynccontextmanager
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# Initialize OpenTelemetry
# Acquire a tracer
tracer = trace.get_tracer(__name__)


# roll
@tracer.start_as_current_span("roll_d6")
def roll_d6():
  value = random.randint(1, 6)
  logger.info(f"Rolled a {value}")
  match value:
    case 6:
        sleep(4)
    case 1: 
        sleep(2)
    
  return value
    
app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
def root():
    return "Welcome to Now Playing!"


@app.post("/nowplaying", status_code = status.HTTP_201_CREATED)
@tracer.start_as_current_span("add_song")
async def now_playing(song: Song):
    with Session(engine) as session:
        session.add(song)
        session.commit()
        session.refresh(song)
        return song
    logger.info("Song added to database")

@app.get("/users/{user_id}/songs")
def get_songs_by_user(user_id: int):
    with Session(engine) as session:
        statement = select(Song).where(Song.user_id == user_id)
        results = session.exec(statement).all()
        return results

@app.get("/health", status_code=200)
def health(response: Response):
    roll = roll_d6()
    match roll:
        case 6:
            logger.info(f"Rolled a {roll}")
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"message": "Internal Server Error"}
        case 1:
            response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            return {"message": "Service Unavailable"}
        case _:
            return {"message": "OK"}