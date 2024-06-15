from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_bcrypt import check_password_hash
from flask_socketio import SocketIO
from Model import db
import os

app = Flask(__name__)

pathOfCurrentDirectory = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(pathOfCurrentDirectory, 'myDatabase.db') # this configures the database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'bad_secret_key'
app.config["JWT_SECRET_KEY"] = 'bad_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}},
     support_credentials=True,
     headers=['Content-Type', 'Authorization'])

api = Api(app)

db.init_app(app)

jwt = JWTManager(app)

socketio = SocketIO(app, cors_allowed_origins="*")

# with app.app_context():
#     db.create_all()
#     db.session.commit()


