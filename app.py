from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from resources import *
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_bcrypt import check_password_hash
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

@app.route('/')
def home():
    return "Backend server is running!"


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print('Received data:', username, password)

    user = db.session.scalars(db.select(User).where(User.username == username)).first()

    if user and user.password == password: #check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print('Received data:', username, password)

    user = db.session.scalars(db.select(User).where(User.username == username)).first()

    if user: #check_password_hash(user.password, password):
        return jsonify({'message': 'Login Failed: username not available'}), 401
    else:
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})


api = Api(app)

db.init_app(app)

jwt = JWTManager(app)

api.add_resource(BookListResources, '/books/<argument>')
api.add_resource(BookResource, '/book/<id>')
api.add_resource(CharacterListResources, '/characters/<argument>')
api.add_resource(CharacterResource, '/character/<id>')
api.add_resource(PingResource, '/ping')

# with app.app_context():
#     db.create_all()
#     db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)


