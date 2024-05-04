from unittest import TestCase
from unittest import main
from flask import Flask
from flask_restful import Api
from Backend.resources import *
import os
from flask_cors import CORS


class TestApi(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True

        self.pathOfCurrentDirectory = os.path.abspath(os.path.dirname(__file__))
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(self.pathOfCurrentDirectory, 'testDatabase.db')  # this configures the database connection string
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        CORS(self.app)
        self.api = Api(self.app)

        self.db = db

        self.db.init_app(self.app)

        self.api.add_resource(BookListResources, '/books/<argument>')
        self.api.add_resource(BookResource, '/book/<id>')
        self.api.add_resource(CharacterListResources, '/characters/<argument>')
        self.api.add_resource(CharacterResource, '/character/<id>')
        self.api.add_resource(PingResource, '/ping')

        with self.app.app_context():
            self.db.create_all()
            self.db.session.commit()

    def tearDown(self):
        # doesn't work because the file PyCharm is using the file
        #os.remove(os.path.join(self.pathOfCurrentDirectory, 'testDatabase.db'))
        with self.app.app_context():
            self.db.session.query(Character).delete()
            self.db.session.query(Book).delete()
            self.db.session.commit()

    def test_get_all_books(self):
        with self.app.test_client() as client:
            response = client.get('/books/optionalArgument')
            TestCase.assertEqual(self, response.status_code, 200)
            TestCase.assertEqual(self, response.json, [])

    def test_get_all_characters(self):
        with self.app.test_client() as client:
            response = client.get('/characters/optionalArgument')
            TestCase.assertEqual(self, response.status_code, 200)
            TestCase.assertEqual(self, response.json, [])

    def test_add_book(self):
        with self.app.test_client() as client:
            response = client.post('/books/nothing', json={"title": "book", "rating": 4})
            TestCase.assertEqual(self, response.status_code, 200)
            x = self.db.session.scalars(db.select(Book)).all()
            TestCase.assertEqual(self, len(x), 1)

    def test_add_character(self):
        with self.app.test_client() as client:
            client.post('/books/nothing', json={"title": "book", "rating": 4})
            response = client.post('/characters/nothing', json={"name": "character", "book_id": 1})
            TestCase.assertEqual(self, response.status_code, 200)
            x = self.db.session.scalars(db.select(Book)).all()
            TestCase.assertEqual(self, len(x), 1)

    def test_get_book(self):
        with self.app.app_context():
            self.db.session.add(Book(title="asda", rating=3))
            db.session.commit()
            with self.app.test_client() as client:
                response = client.get('/book/1')
                TestCase.assertEqual(self, response.status_code, 200)
                TestCase.assertEqual(self, {"id": 1, "title": "asda", "rating": 3}, response.json)

    def test_get_character(self):
        with self.app.app_context():
            self.db.session.add(Book(title="asda", rating=3))
            self.db.session.add(Character(name="c", book_id=1))
            db.session.commit()
            with self.app.test_client() as client:
                response = client.get('/character/1')
                TestCase.assertEqual(self, response.status_code, 200)
                TestCase.assertEqual(self, {"id": 1, "name": "c", "book_id": 1}, response.json)

    def test_update_book(self):
        with self.app.app_context():
            self.db.session.add(Book(title="book", rating=5))
            db.session.commit()
        with self.app.test_client() as client:
            response = client.put('/book/1', json={"title": "book1", "rating": 3})
            TestCase.assertEqual(self, response.status_code, 200)
            book = db.session.scalars(db.select(Book).where(Book.id == 1)).first()
            TestCase.assertEqual(self, book.title, "book1")
            TestCase.assertEqual(self, book.rating, 3)

    def test_update_character(self):
        with self.app.app_context():
            self.db.session.add(Book(title="book", rating=5))
            self.db.session.add(Book(title="book2", rating=5))
            self.db.session.add(Character(name="c", book_id=1))
            db.session.commit()
        with self.app.test_client() as client:
            response = client.put('/character/1', json={"name": "c2", "book_id": 2})
            TestCase.assertEqual(self, response.status_code, 200)
            character = db.session.scalars(db.select(Character).where(Character.id == 1)).first()
            TestCase.assertEqual(self, character.name, "c2")
            TestCase.assertEqual(self, character.book_id, 2)

    def test_delete_book(self):
        with self.app.app_context():
            self.db.session.add(Book(title="book", rating=5))
            db.session.commit()
        with self.app.test_client() as client:
            response = client.delete('/book/1')
            TestCase.assertEqual(self, response.status_code, 200)
            TestCase.assertEqual(self, len(db.session.scalars(db.select(Book)).all()), 0)

    def test_delete_book(self):
        with self.app.app_context():
            self.db.session.add(Book(title="book", rating=5))
            self.db.session.add(Character(name="c", book_id=1))
            db.session.commit()
        with self.app.test_client() as client:
            response = client.delete('/character/1')
            TestCase.assertEqual(self, response.status_code, 200)
            TestCase.assertEqual(self, len(db.session.scalars(db.select(Character)).all()), 0)

if __name__ == "__main__":
    main()
