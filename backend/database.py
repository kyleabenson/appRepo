from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
    songs: List["Song"] = Relationship(back_populates="user")


class Song(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    artist: str
    url: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="songs")


engine = create_engine("sqlite:///database.db")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
