import flask
from flask_restful import Resource
from Backend.repository import *
from Backend.Model import *
from Backend.auxiliary import *

data = Repository()


# not needed anymore because we are using an ORM instead of a repository
def check_if_book_exists(id):
    if not data.checkExistence(id):
        simple_message_error("Book with ID {} doesn't exist.".format(id))


class BookResource(Resource):
    def delete(self, id):
        id = int(id)
        #check_if_book_exists(id)
        book = db.session.scalars(db.select(Book).where(Book.id == id)).first()
        db.session.delete(book)
        db.session.commit()
        return simple_message_response("Book with ID {} has been deleted.".format(id), 200)

    def get(self, id):
        id = int(id)
        response = db.session.scalars(db.select(Book).where(Book.id == id)).first()
        print(response)
        response = response.serialize()
        print(response)
        return response

    def put(self, id):
        id = int(id)
        #check_if_book_exists(id)
        args = bookParser.parse_args()
        print(args)

        book = db.session.scalars(db.select(Book).where(Book.id == id)).first()
        book.title = args['title']
        book.rating = args['rating']
        db.session.commit()
        return simple_message_response("Book with ID {} has been updated.".format(id), 200)

class CharacterResource(Resource):
    def get(self, id):
        id = int(id)
        response = db.session.scalars(db.select(Character).where(Character.id == id)).first()
        response = response.serialize()
        print(response)
        return response

    def put(self, id):
        id = int(id)
        args = characterParser.parse_args()
        print(args)

        character = db.session.scalars(db.select(Character).where(Character.id == id)).first()
        character.name = args['name']
        character.book_id = args['book_id']
        print(character.book)
        db.session.commit()
        return simple_message_response(f"Character with ID {id} has been updated.")

    def delete(self, id):
        id = int(id)
        character = db.session.scalars(db.select(Character).where(Character.id == id)).first()
        db.session.delete(character)
        db.session.commit()
        return simple_message_response("Character with ID {} has been deleted.".format(id), 200)



# This is the resource that will be used to handle multiple books.
class BookListResources(Resource):
    def post(self, argument):
        args = bookParser.parse_args()
        response = db.session.add(Book(title=args['title'], rating=args['rating']))
        db.session.commit()
        return response

    def get(self, argument):
        try:
            response = None
            if argument == 'titles':
                response = db.session.scalars(db.select(Book.title)).all()
                return response
            elif argument == 'ratings':
                response = db.session.scalars(db.select(Book.rating)).all()
                return response
            elif argument == 'sorted':
                response = db.session.scalars(db.select(Book).order_by(Book.rating)).all()
                print(response)
                return [element.serialize() for element in response]
            else:
                response = db.session.scalars(db.select(Book)).all()
                return [element.serialize() for element in response]
        except Exception as error:
            return simple_message_error(f"Error on fetch books: {error}")


class CharacterListResources(Resource):
    def post(self, argument):
        args = characterParser.parse_args()
        response = db.session.add(Character(name=args['name'], book_id=args['book_id']))
        db.session.commit()
        return response

    def get(self, argument):
        try:
            response = db.session.scalars(db.select(Character)).all()
            return [element.serialize() for element in response]
        except Exception as error:
            return simple_message_error(f"Error on fetch characters: {error}")


class PingResource(Resource):
    def get(self):
        return simple_message_response("Ping successfully delivered", 200)


def jsonify_and_add_proper_header(response):
    response = flask.jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Credentials', 'true')
    return response
