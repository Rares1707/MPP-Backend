import flask
from flask import Flask
from flask_restful import Resource, Api
from projectFiles.repository import *
from projectFiles.Book import *
from projectFiles.auxiliary import *
from flask_cors import CORS

MAX_PAGE_SIZE = 36
DEFAULT_PAGE_SIZE = 6

data = Repository()

app = Flask(__name__)
CORS(app)
api = Api(app)


# This is the resource that will be used to handle one book.
def check_if_book_exists(id):
    if not data.checkExistence(id):
        simple_message_error("Book with ID {} doesn't exist.".format(id))


class BookResource(Resource):
    def delete(self, id):
        id = int(id)
        check_if_book_exists(id)
        data.remove(id)
        return simple_message_response("Book with ID {} has been deleted.".format(id), 200)

    def get(self, id):
        id = int(id)
        check_if_book_exists(id)
        return data.get(id).serialize()

    def put(self, id):
        id = int(id)
        check_if_book_exists(id)
        args = bookParser.parse_args()
        print(args)
        data.update(id, Book(args['title'], args['rating']))
        return simple_message_response("Book with ID {} has been updated.".format(id), 200)

# This is the resource that will be used to handle multiple books.
class BookListResources(Resource):
    def post(self, argument):
        args = bookParser.parse_args()
        response = data.insert(Book(args['title'], args['rating'])).serialize()
        print(response)
        return jsonify_and_add_proper_header(response)

    # Paged get.
    #def get(self):
        # Get page size from request.
        #pageSize = int(request.args["pageSize"]) if "pageSize" in request.args else DEFAULT_PAGE_SIZE
        #pageSize = min(MAX_PAGE_SIZE, pageSize)

        # Get page offset from request.
        #pageOffset = int(request.args["pageOffset"]) if "pageOffset" in request.args else 0

        #return [e.serialize() for e in data.get_paged(size=pageSize, offset=pageOffset)]

    def get(self, argument):
        if argument == 'titles':
            response = data.get_titles()
            return jsonify_and_add_proper_header(response)
        if argument == 'ratings':
            response = data.get_ratings()
            return jsonify_and_add_proper_header(response)
        if argument == 'sorted':
            data.sort_List()
        bookList = data.get_all()
        response = [book.serialize() for book in bookList]
        return jsonify_and_add_proper_header(response)



def jsonify_and_add_proper_header(response):
    response = flask.jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Credentials', 'true')
    #response.headers.add('Access-Control-Allow-Origin: *')
    #response.headers.add('Access-Control-Allow-Methods', '*')
    #response.headers.add('Access-Control-Allow-Headers: *')
    #header('Access-Control-Max-Age: 1728000')
    #header("Content-Length: 0")
    #header("Content-Type: text/plain")
    return response
