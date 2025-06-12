from sqlmodel import Field, Session, SQLModel, create_engine


class Song(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    artist: str
    url: str
    user_id: int


engine = create_engine("sqlite:///database.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
