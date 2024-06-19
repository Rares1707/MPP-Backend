from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from resources import *
from flask_jwt_extended import jwt_required, create_access_token
from flask_bcrypt import check_password_hash, generate_password_hash
from app_initialization import socketio, api, app

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

    if user and check_password_hash(user.password, password):
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

    if user:
        return jsonify({'message': 'Login Failed: username not available'}), 401
    else:
        encrypted_password = generate_password_hash(password)
        new_user = User(username=username, password=encrypted_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})


@app.route('/userCreationDate', methods=['GET'])
@jwt_required()
def getUserCreationDate():
    id = get_jwt_identity()
    user = db.session.scalars(db.select(User).where(User.id == id)).first()
    response = jsonify(user.dateCreated)
    print(response)
    return response



#socketio = SocketIO(cors_allowed_origins="*") #if 'socketio' not in locals() else socketio


#api.add_resource(BookListResources, '/books?type=<type>&page=<page>&pageSize=<pageSize>')
api.add_resource(BookListResources, '/books')
api.add_resource(BookResource, '/book/<id>')
api.add_resource(CharacterListResources, '/characters/<argument>')
api.add_resource(CharacterResource, '/character/<id>')
api.add_resource(PingResource, '/ping')

# with app.app_context():
#     db.create_all()
#     db.session.commit()

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, port=5000)
    #app.run(debug=True, port=5000)


