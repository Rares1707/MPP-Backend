from app import db, app
from Model import Book
from Model import User
from Model import Character
from sqlalchemy import insert
from random import choice
from faker import Faker


NUMBER_OF_EPOCHS = 100000

myFaker = Faker()


def insert_fake_books_in_database():
    books = []
    for i in range(NUMBER_OF_EPOCHS):
        books.append(Book.generate_fake(Book))
    db.session.bulk_save_objects(books) #outdated but working
    #db.session.execute(insert(Book), books) #new but needs JSONs or smth
    db.session.commit()


def insert_fake_characters_in_database():
    books = db.session.scalars(db.select(Book)).all()
    book_ids = [book.id for book in books]
    characters = []
    for i in range(NUMBER_OF_EPOCHS):
        characters.append(Character(name=myFaker.name(), book_id=choice(book_ids)))
    db.session.bulk_save_objects(characters) #outdated but working
    #db.session.execute(insert(Character), characters) #new but needs JSONs or smth
    db.session.commit()


if __name__=="__main__":
    with app.app_context():
        db.create_all()
        #db.session.commit()
        #db.session.add(User(username="admin", password="admin", is_admin=True))
        #db.session.add(User(username="a", password="a", is_admin=True))
        #db.session.add(User(username="u3", password="p3", is_admin=False))

        #db.session.add(Book(title="b1", rating=3.4, user_id=3))
        #insert_fake_books_in_database()
        insert_fake_characters_in_database()
        db.session.commit()

        #flask db migrate
