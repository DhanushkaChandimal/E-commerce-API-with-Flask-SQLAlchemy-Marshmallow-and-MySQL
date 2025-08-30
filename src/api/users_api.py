from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from ..app_config import app, db
from ..models.user import User
from ..schemas import user_schema, users_schema
from flask_jwt_extended import create_access_token, jwt_required
from ..config import AUTH

# BONUS TASK: Add JWT authentication for user operations
@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if not email == AUTH["email"] or not password == AUTH["password"]:
        return jsonify({"msg": "Bad credentials"}), 401
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200

@app.route('/users', methods = ['GET'])
@jwt_required()
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200

@app.route('/users/<int:id>', methods = ['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

@app.route('/users', methods = ['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_user = User(name=user_data['name'], address=user_data['address'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@app.route('/users/<int:id>', methods = ['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.name = user_data['name']
    user.address = user_data['address']
    user.email = user_data['email']
    db.session.commit()
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted user {id}"}), 200