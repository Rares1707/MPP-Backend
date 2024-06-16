import flask
from flask_restful import Resource
from repository import *
from Model import *
from auxiliary import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from app_initialization import socketio
from flask import request

# not needed anymore
data = Repository()


# not needed anymore because we are using an ORM instead of a repository
def check_if_book_exists(id):
    if not data.checkExistence(id):
        simple_message_error("Book with ID {} doesn't exist.".format(id))


def broadcast_refresh():
    socketio.emit('refresh', '')  # first parameter is the event name, second parameter is the data to be sent


# DON'T USE method_decorators = [jwt_required()] FOR ANY OF THE RESOURCES
# BECAUSE IT WILL OVERRIDE THE OTHER HEADERS (SUCH AS THE CORS HEADER)

class BookResource(Resource):
    @jwt_required()
    def delete(self, id):
        book_id = int(id)
        user_id = get_jwt_identity()
        user = db.session.scalars(db.select(User).where(User.id == user_id)).first()
        #check_if_book_exists(id)
        book = db.session.scalars(db.select(Book).where(Book.id == book_id)).first()
        if user.is_admin or book.user_id == user_id:
            db.session.delete(book)
            db.session.commit()
            broadcast_refresh()
            return simple_message_response("Book with ID {} has been deleted.".format(book_id), 200)
        return simple_message_response("Book with ID {} has not been deleted.".format(book_id), 200)

    @jwt_required()
    def get(self, id):
        book_id = int(id)
        user_id = get_jwt_identity()
        user = db.session.scalars(db.select(User).where(User.id == user_id)).first()
        book = db.session.scalars(db.select(Book).where(Book.id == book_id)).first()

        if user.is_admin or book.user_id == user_id:
            response = book.serialize()
            return response
        return simple_message_error("You are not allowed to access this book.", 401)

    @jwt_required()
    def put(self, id):
        #print('here')
        book_id = int(id)
        #check_if_book_exists(id)
        args = bookParser.parse_args()
        print(args)

        user_id = get_jwt_identity()
        user = db.session.scalars(db.select(User).where(User.id == user_id)).first()

        book = db.session.scalars(db.select(Book).where(Book.id == book_id)).first()
        if user.is_admin or book.user_id == user_id:
            book.title = args['title']
            book.rating = args['rating']
            db.session.commit()
            broadcast_refresh()
            return simple_message_response("Book with ID {} has been updated.".format(book_id), 200)
        return simple_message_error("You are not allowed to update this book.", 401)


class CharacterResource(Resource):
    @jwt_required()
    def get(self, id):
        id = int(id)
        response = db.session.scalars(db.select(Character).where(Character.id == id)).first()
        response = response.serialize()
        print(response)
        return response

    @jwt_required()
    def put(self, id):
        id = int(id)
        args = characterParser.parse_args()
        print(args)

        character = db.session.scalars(db.select(Character).where(Character.id == id)).first()
        character.name = args['name']
        character.book_id = args['book_id']
        print(character.book)
        db.session.commit()
        broadcast_refresh()
        return simple_message_response(f"Character with ID {id} has been updated.")

    @jwt_required()
    def delete(self, id):
        id = int(id)
        character = db.session.scalars(db.select(Character).where(Character.id == id)).first()
        db.session.delete(character)
        db.session.commit()
        broadcast_refresh()
        return simple_message_response("Character with ID {} has been deleted.".format(id), 200)


def getIndexOfRequestedPage():
    return request.args.get('page', default=1, type=int)


def getSizeOfRequestedPage():
    return request.args.get('pageSize', default=3, type=int)


def getTypeOfGetRequest():
    return request.args.get('type', default='notSorted', type=str)


# This is the resource that will be used to handle multiple books.
class BookListResources(Resource):
    @jwt_required()
    def post(self):
        args = bookParser.parse_args()
        print(args)
        user_id = get_jwt_identity()
        response = db.session.add(Book(title=args['title'], rating=args['rating'], user_id=user_id))
        print(response)
        db.session.commit()
        broadcast_refresh()
        return response

    @jwt_required()
    def get(self):
        print('hereeeeee')
        typeOfRequest = request.args.get('type', default='notSorted', type=str)
        user_id = get_jwt_identity()
        user = db.session.scalars(db.select(User).where(User.id == user_id)).first()
        print(typeOfRequest)
        print(user)
        try:
            response = None
            if typeOfRequest == 'titles' and user.is_admin:
                response = db.session.scalars(db.select(Book.title)).all()
                return response
            elif typeOfRequest == 'titles' and not user.is_admin:
                response = db.session.scalars(db.select(Book.title).where(Book.user_id == user_id)).all()
                return response

            elif typeOfRequest == 'ratings' and user.is_admin:
                print(user.is_admin)
                response = db.session.scalars(db.select(Book.rating)).all()
                return response
            elif typeOfRequest == 'ratings' and not user.is_admin:
                response = db.session.scalars(db.select(Book.rating).where(Book.user_id == user_id)).all()
                return response

            elif typeOfRequest == 'sorted' and user.is_admin:
                response = db.paginate(db.select(Book).order_by(Book.rating),
                                       page=request.args.get('page', default=1, type=int),
                                       per_page=request.args.get('pageSize', default=3, type=int))
                return [element.serialize() for element in response]
            elif typeOfRequest == 'sorted' and not user.is_admin:
                response = db.paginate(db.select(Book).
                                       where(Book.user_id == user_id).
                                       order_by(Book.rating),
                                       page=request.args.get('page', default=1, type=int),
                                       per_page=request.args.get('pageSize', default=3, type=int))
                return [element.serialize() for element in response]

            elif user.is_admin:
                print('a')
                print(request.args.get('pageSize', default=1, type=int))
                response = db.paginate(db.select(Book),  #db.session.scalars(db.select(Book)).all,
                                       page=request.args.get('page', default=1, type=int),
                                       per_page=request.args.get('pageSize', default=3, type=int))
                print('b')
                print([element.serialize() for element in response])
                return [element.serialize() for element in response]
            elif not user.is_admin:
                response = db.paginate(db.select(Book).where(Book.user_id == user_id),
                                       #db.session.scalars(db.select(Book).where(Book.user_id == user_id)).all(),
                                       page=request.args.get('page', default=1, type=int),
                                       per_page=request.args.get('pageSize', default=3, type=int))
                return [element.serialize() for element in response]
        except Exception as error:
            return simple_message_error(f"Error on fetch books: {error}")


class CharacterListResources(Resource):
    @jwt_required()
    def post(self, argument):
        args = characterParser.parse_args()
        response = db.session.add(Character(name=args['name'], book_id=args['book_id']))
        db.session.commit()
        broadcast_refresh()
        return response

    @jwt_required()
    def get(self, argument):
        try:
            response = db.session.scalars(db.select(Character)).all()
            return [element.serialize() for element in response]
        except Exception as error:
            return simple_message_error(f"Error on fetch characters: {error}")


class PingResource(Resource):
    def get(self):
        return simple_message_response("Ping successfully delivered", 200)


class UserResource(Resource):
    def post(self):
        args = userParser.parse_args()
        response = db.session.add(User(username=args['username'], password=args['password']))
        db.session.commit()
        broadcast_refresh()
        return response

    def get(self):
        id = get_jwt_identity()
        response = db.session.scalars(db.select(User).where(User.id == id)).first()
        response = response.serialize()
        print(response)
        return response


def jsonify_and_add_proper_header(response):
    response = flask.jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Credentials', 'true')
    return response
