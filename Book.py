from flask_restful import reqparse


class Book:
    def __init__(self, title, rating):
        self._id = None                  # This is not set by the user, should be set at insertion.
        self._title = title
        self._rating = rating

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        self._rating = rating

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


bookParser = reqparse.RequestParser()
bookParser.add_argument('title', type=str)
bookParser.add_argument('rating', type=float)