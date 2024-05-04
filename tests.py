import unittest
from Backend.resources import *


class TestRepository(unittest.TestCase):
    def test_add_to_repo(self):
        data.clear()
        data.insert(Book("Book 1", 5))
        data.insert(Book("Book 2", 2))
        unittest.TestCase.assertEqual(self, len(data.get_all()), 2)

    def test_remove_from_repo(self):
        data.clear()
        data.insert(Book("Book 1", 5))
        data.insert(Book("Book 2", 2))
        data.remove(1)
        unittest.TestCase.assertEqual(self, len(data.get_all()), 1)
        unittest.TestCase.assertEqual(self, data.get(1), None)

    def test_update_repo(self):
        data.clear()
        data.insert(Book("Book 1", 5))
        data.insert(Book("Book 2", 2))
        book = data.get(1)
        unittest.TestCase.assertEqual(self, book.title, "Book 1")
        unittest.TestCase.assertEqual(self, book.rating, 5)


class TestService(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.api = Api(self.app)

        self.api.add_resource(BookListResources, '/books/<arguments>')
        self.api.add_resource(BookResource, '/book/<id>')

    def test_get_all_books(self):
        self.setUp()
        data.clear()
        with self.app.test_client() as client:
            response = client.get('/books/nothing')
            unittest.TestCase.assertEqual(self, response.status_code, 200)
            unittest.TestCase.assertEqual(self, response.json, [])

    def test_add_book(self):
        self.setUp()
        data.clear()
        with self.app.test_client() as client:
            response = client.post('/books/nothing', json={"title": "book", "rating": 4})
            unittest.TestCase.assertEqual(self, response.status_code, 200)
            unittest.TestCase.assertEqual(self, len(data.get_all()), 1)

    def test_get_book(self):
        data.insert(Book("Book 1", 5))
        with self.app.test_client() as client:
            response = client.get('/book/1')
            unittest.TestCase.assertEqual(self, response.status_code, 200)
            unittest.TestCase.assertEqual(self, response.json, {"id": 1, "title": "Book 1", "rating": 5})

    def test_update_book(self):
        data.insert(Book("book", 5))
        with self.app.test_client() as client:
            response = client.put('/book/1', json={"title": "book1", "rating": 3})
            print(response)
            unittest.TestCase.assertEqual(self, response.status_code, 200)
            book = data.get(1)
            unittest.TestCase.assertEqual(self, book.title, "book1")
            unittest.TestCase.assertEqual(self, book.rating, 3)

    def test_delete_book(self):
        with self.app.test_client() as client:
            response = client.delete('/book/1')
            unittest.TestCase.assertEqual(self, response.status_code, 200)
            unittest.TestCase.assertEqual(self, len(data.get_all()), 0)



if __name__ == "__main__":
    unittest.main()
