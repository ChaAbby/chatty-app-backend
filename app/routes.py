from flask import Blueprint, request, jsonify
from .models import User
 
main = Blueprint('main', __name__)
 
@main.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User.create(data['username'], data['email'])
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