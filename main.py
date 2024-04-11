from flask import Flask
from flask_restful import Api
from resources import *

if __name__ == '__main__':
    api.add_resource(BookListResources, '/books/<argument>')
    api.add_resource(BookResource, '/book/<id>')

    app.run(debug=True, port=5000)
