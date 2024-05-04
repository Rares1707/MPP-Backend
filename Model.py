from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from typing import List
import random
from flask_restful import reqparse
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from faker import Faker
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

fakeBookGenerator = Faker()
fakeCharacterGenerator = Faker()

bookParser = reqparse.RequestParser()
bookParser.add_argument('title', type=str)
bookParser.add_argument('rating', type=float)

characterParser = reqparse.RequestParser()
characterParser.add_argument('name', type=str)
characterParser.add_argument('book_id')

class Book(db.Model):
    __tablename__ = 'books_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    #id = db.Column(db.Integer, db.Identity(), primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    #title = db.Column(db.String(50), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    #rating = db.Column(db.Integer, nullable=False)

    characters: Mapped[List["Character"]] = relationship(
        back_populates="book", cascade="all, delete-orphan")
    #characters = relationship('Character', back_populates='book')

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

    def generate_fake(self):
        return Book(title=fakeBookGenerator.name(), rating=random.randrange(0, 5))


class Character(db.Model):
    __tablename__ = 'characters_table'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    #id = db.Column(db.Integer, db.Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    #name = db.Column(db.String(50), nullable=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("books_table.id"))
    #book_id = db.Column(db.Integer, ForeignKey('books.id'))

    book: Mapped["Book"] = relationship(back_populates="characters")
    #book = relationship('Book', back_populates='characters')

    def __repr__(self) -> str:
        ...
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

    #def generate_fake(self):
        #return Character(name=fakeCharacterGenerator.name())

