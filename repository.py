from Model import Book


class Repository:
    def __init__(self):
        self._data = []
        self._next_id = 1
        self._populate()

    def clear(self):
        self._data = []
        self._next_id = 1

    def insert(self, obj):
        obj.id = self._next_id
        self._next_id += 1
        self._data.append(obj)
        return obj

    def checkExistence(self, id):
        for object in self._data:
            if object.id == id:
                return True
        return False

    def get(self, id):
        for object in self._data:
            if object.id == id:
                return object
        return None

    def remove(self, id):
        for object in self._data:
            if object.id == id:
                self._data.remove(object)
                return

    def update(self, id, newInstance):
        newInstance.id = id
        for object in self._data:
            if object.id == newInstance.id:
                object.deep_copy(newInstance)

    def get_paged(self, size, offset=0):
        return self._data[offset:offset + size]

    def get_all(self):
        return self._data

    def sort_List(self):
        self._data.sort(key=lambda book: book.rating)

    def get_titles(self):
        titles = [book.title for book in self._data]
        return titles

    def get_ratings(self):
        ratings = [book.rating for book in self._data]
        return ratings

    def _populate(self):
        pass
        # self.insert(Book("Harry Potter", 4.8))
        # self.insert(Book("The Hobbit", 4.3))
        # self.insert(Book("The Great Gatsby", 4.2))
        # self.insert(Book("To Kill a Mockingbird", 4.5))
        # self.insert(Book("1984", 4.6))
        # self.insert(Book("Pride and Prejudice", 4.7))
        # self.insert(Book("The Catcher in the Rye", 4.1))
        # self.insert(Book("The Lord of the Rings", 4.9))
        # self.insert(Book("Animal Farm", 4.4))
        # self.insert(Book("Brave New World", 4.3))
        # self.insert(Book("Fahrenheit 451", 4.2))
        # self.insert(Book("The Grapes of Wrath", 4.0))
        # self.insert(Book("The Scarlet Letter", 3.8))
        # self.insert(Book("The Odyssey", 4.5))
        # self.insert(Book("The Picture of Dorian Gray", 4.4))
        # self.insert(Book("The Adventures of Huckleberry Finn", 4.6))
        # self.insert(Book("The Count of Monte Cristo", 4.7))
        # self.insert(Book("The Brothers Karamazov", 4.5))
        # self.insert(Book("Crime and Punishment", 4.6))
        # self.insert(Book("The Road", 4.0))
