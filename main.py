from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from resources import *
import os

app = Flask(__name__)

pathOfCurrentDirectory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(pathOfCurrentDirectory, 'myDatabase.db') # this configures the database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

api = Api(app)

db.init_app(app)

CORS(app)

api.add_resource(BookListResources, '/books/<argument>')
api.add_resource(BookResource, '/book/<id>')
api.add_resource(CharacterListResources, '/characters/<argument>')
api.add_resource(CharacterResource, '/character/<id>')
api.add_resource(PingResource, '/ping')


if __name__ == '__main__':
    app.run(debug=True, port=5000)


