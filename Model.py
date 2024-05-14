from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, DateTime, ForeignKey
from typing import List
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

bookParser = reqparse.RequestParser()
bookParser.add_argument('title', type=str)
bookParser.add_argument('rating', type=float)

characterParser = reqparse.RequestParser()
characterParser.add_argument('name', type=str)
characterParser.add_argument('book_id')

userParser = reqparse.RequestParser()
userParser.add_argument('username', type=str)
userParser.add_argument('password', type=str)

class Book(db.Model):
    __tablename__ = 'books_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

    characters: Mapped[List["Character"]] = relationship(back_populates="book", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, rating={self.rating!r})"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "rating": self.rating,
        }

    def deep_copy(self, other):
        self.id = other.id
        self.title = other.title
        self.rating = other.rating
        self.characters = other.characters


class Character(db.Model):
    __tablename__ = 'characters_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books_table.id"))

    book: Mapped["Book"] = relationship(back_populates="characters")

    def __repr__(self) -> str:
        return f"Character(id={self.id!r}, name={self.name!r}, book_id={self.book_id!r})"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "book_id": self.book_id
        }

    def deep_copy(self, other):
        self.id = other.id
        self.name = other.name
        self.book_id = other.book_id
        self.book = other.book


class User(db.Model):
    __tablename__ = 'users_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    dateCreated: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, dateCreated={self.dateCreated!r})"

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "dateCreated": self.dateCreated
        }

    def deep_copy(self, other):
        self.id = other.id
        self.username = other.username
        self.password = other.password
        self.dateCreated = other.dateCreated
