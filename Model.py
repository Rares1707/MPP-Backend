from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from typing import List
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from random import choice


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

bookParser = reqparse.RequestParser()
bookParser.add_argument('title', type=str)
bookParser.add_argument('rating', type=float)
bookParser.add_argument('user_id', type=int)

characterParser = reqparse.RequestParser()
characterParser.add_argument('name', type=str)
characterParser.add_argument('book_id')

userParser = reqparse.RequestParser()
userParser.add_argument('username', type=str)
userParser.add_argument('password', type=str)
userParser.add_argument('is_admin', type=bool)

myFaker = Faker()

class Book(db.Model):
    __tablename__ = 'books_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

    characters: Mapped[List["Character"]] = relationship(back_populates="book", cascade="all, delete-orphan")

    user_id: Mapped[int] = mapped_column(ForeignKey("users_table.id"))
    user: Mapped["User"] = relationship(back_populates="books")

    MINIMUM_RATING = 1
    MAXIMUM_RATING = 5

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, title={self.title!r}, rating={self.rating!r}, user_id={self.user_id!r})"

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

    @staticmethod
    def generate_fake(thisClass):
        return Book(title=myFaker.name(), rating=myFaker.random_int(thisClass.MINIMUM_RATING, thisClass.MAXIMUM_RATING),
                    user_id=1)


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

    @staticmethod
    def generate_fake(): #this becomes way too slow if there are many books
        books = db.session.scalars(db.select(Book)).all()
        book_ids = [book.id for book in books]
        return Character(name=myFaker.name(), book_id=choice(book_ids))

class User(db.Model):
    __tablename__ = 'users_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    dateCreated: Mapped[datetime] = mapped_column(DateTime, default=datetime.today())
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    books: Mapped[List["Book"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, password={self.password!r}, dateCreated={self.dateCreated!r}, is_admin={self.is_admin!r})"

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


