from time import sleep
import random
import logging
from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace
from sqlmodel import Session, select
from .database import Song, User, engine, create_db_and_tables
from contextlib import asynccontextmanager
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


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

def get_current_user(token: str = Depends(oauth2_scheme)):
    with Session(engine) as session:
        statement = select(User).where(User.username == token)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

@app.post("/register")
def register_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        statement = select(User).where(User.username == form_data.username)
        user = session.exec(statement).first()
        if not user or user.password != form_data.password:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        return {"access_token": user.username, "token_type": "bearer"}

@app.get("/")
def root():
    return "Welcome to Now Playing!"


@app.post("/nowplaying", status_code = status.HTTP_201_CREATED)
@tracer.start_as_current_span("add_song")
async def now_playing(song: Song, current_user: User = Depends(get_current_user)):
    song.user_id = current_user.id
    with Session(engine) as session:
        session.add(song)
        session.commit()
        session.refresh(song)
        return song
    logger.info("Song added to database")

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user



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