from datetime import datetime
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserModel(SQLModel): # "Basis" – nur Felder, KEINE Tabelle
    username: str
    email: EmailStr
    password: str
    name: str


class UserTable(UserModel, table=True): # "Tabelle" – erbt von UserModel
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: list["PostTable"] = Relationship(back_populates="author")


class PostModel(SQLModel):
    content: str
    created_at: datetime = Field(default_factory=datetime.now)


class PostTable(PostModel, table=True):
    __tablename__ = "posts"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    author: Optional[UserTable] = Relationship(back_populates="posts")
