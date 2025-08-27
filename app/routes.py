from flask import Blueprint, request, jsonify
from .models import *
 
main = Blueprint('main', __name__)

# Users Routes
@main.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User.create(data['username'], data['email'], data["password"], data['lastSeen'],data["avatarUrl"], data['role'],)
    return jsonify(user), 201
 
@main.route('/users/<username>', methods=['GET'])
def get_user(username):
    user = User.get_by_username(username)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404
 
@main.route('/users/<username>', methods=['PUT'])
def update_user(username):
    data = request.json
    User.update(username, data['email'])
    return jsonify({'message': 'User updated'}), 200
 
@main.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    User.delete(username)
    return jsonify({'message': 'User deleted'}), 200

@main.route('/users/<user_id>/chats', methods=["GET"])
def get_specific_users_chats(user_id):
    chats = Chat.get_by_user_id(user_id)
    if chats:
        return jsonify(chats), 200
    return jsonify({'error': "User not found"}), 404

# Chats Routes
@main.route('/chats', methods=["POST"])
def create_chat():
    data = request.json
    print(data)
    if "name" not in data:
        data["name"] = None

    chat = Chat.create(data['name'], data['ownerId'], data['isGroup'], data['members'], data["createdAt"],data['active'])
    return jsonify(chat), 201

@main.route('/chats/<id>', methods=["GET"])
def get_chat_details(id):
    chat = Chat.get_by_id(id)
    if chat:
        return jsonify(chat), 200
    return jsonify({'error': "User not found"}), 404


