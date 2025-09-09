from flask import Blueprint, request, jsonify
import datetime
from .models import *
 
main = Blueprint('main', __name__)

# Users Routes
@main.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data.get('username'):
        return jsonify({'error': 'Username field is required'},400)
    elif not data.get('email'):
        return jsonify({'error': 'Email field is required'}, 400)
    elif not data.get('password'):
        return jsonify({'error': 'Password field is required'}, 400)
    role = data.get('role')

    if not role:
        role = "user"
    elif role != "admin" and role != 'user':
        return jsonify({'error': 'Role must either be "admin" or "user'}, 400)

    user = User.create(data['username'], data['email'], data["password"], data['lastSeen'],data["avatarUrl"], role)
    return jsonify(user), 201

@main.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.get_user(id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User with id: {id} was not found, this user may not exist. Please verify that this is a valid user id'}), 404

@main.route('/users/usernames/<username>', methods=['GET'])
def get_user_by_username(username):
    user = User.get_by_username(username)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404
 
@main.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    if data.get('email'):
        updated_user = User.update(id, data['email'])
    else:
        return jsonify({'message': 'Email is a required field'})

    if updated_user.modified_count:
        return jsonify({'message': f'User with id: {id} was updated'}), 200
    return jsonify({'message': f'User with id: {id} was not updated, please verify that this is a valid user id'})

@main.route('/users/<user_id>/chats', methods=["GET"])
def get_specific_users_chats(user_id):
    chats = Chat.get_by_user_id(user_id)
    if chats:
        return jsonify(chats), 200
    return jsonify({'error': "User not found"}), 404

@main.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    deleted_user = User.delete(id)
    if deleted_user.deleted_count:
        return jsonify({'message': f'User with id: {id} was deleted'}), 200
    return jsonify({'message': f'User with id: {id} was not deleted, please check that this is a valid user id'})

# Chats Routes
@main.route('/chats', methods=["POST"])
def create_chat():
    data = request.json
    if not data.get('name'):
        data["name"] = None

    chat = Chat.create(data['name'], data['ownerId'], data['isGroup'], data['members'], data["createdAt"],data['active'])
    return jsonify(chat), 201

@main.route('/chats/<id>', methods=["GET"])
def get_chat_details(id):
    chat = Chat.get_by_id(id)
    if chat:
        return jsonify(chat), 200
    return jsonify({'error': "Chat not found"}), 404

@main.route("/chats/<id>", methods=["PATCH"])
def update_chat(id):
    data = request.json
    modify_data = {}

    for field in data:
        if data.get(field):
            modify_data[field] = data[field]
        
    modified_fields = Chat.modify_fields(id, modify_data)
    modified_count = modified_fields.modified_count
    if modified_count or modified_fields.matched_count:
        message = ""
        if modified_count > 0:
            message = f"Chat {id} was updated"
        else: 
            message = f"Chat{id} was not updated, request data was identical to database"

        return jsonify({'message': message}, 200)
    
    return jsonify({'message': f'There were issues updating chat {id}'}, 400)

@main.route("/chats/<id>/members", methods=["PATCH"])
def update_chat_members(id):
    data = request.json
    add = data.get('add')
    delete = data.get('delete')

    add_count, delete_count = 0,0
    add_modified_count, delete_modified_count = 0,0
    add_match_count, delete_match_count = 0,0
    if add:
        add_count = len(add)
        added_res = Chat.add_members(id, add)
        add_modified_count = added_res.modified_count
        add_match_count = added_res.matched_count

    if delete:
        delete_count = len(delete)
        deleted_res = Chat.delete_members(id, delete)
        delete_modified_count = deleted_res.modified_count
        delete_match_count = deleted_res.matched_count

    add_success_message = None
    delete_success_message = None
    if add_count == add_modified_count or add_count == add_match_count:
        add_success_message = f'{add_modified_count} member(s) were added'
    if delete_count == delete_modified_count or delete_count == delete_match_count:
        delete_success_message = f'{delete_modified_count} member(s) were deleted'
    if add_success_message and delete_success_message:
        return jsonify({'message':f'Chat {id}: {add_success_message} and {delete_success_message}.'}, 200)
    return jsonify({'message': f'There were issues updating chat {id}. {add_modified_count}/{add_count} were added and {delete_modified_count}/{delete_count} were deleted'}, 400)

@main.route("/chats/<id>", methods=["DELETE"])
def delete_chat(id):
    deleted_chat = Chat.delete(id)
    if deleted_chat.deleted_count:
        return jsonify({'message': f'Chat {id} was deleted'}), 200
    return jsonify({'message': f'Chat {id} was not deleted, please check that this is a valid chat id'},400)

# Messages Route
@main.route('/messages', methods=["POST"])
def create_message():
    data = request.json

    message = Message.create(data['chatId'], data['senderId'], data['content'], data['messageType'], datetime.datetime.now(), None, False, False)
    return jsonify(message), 201

@main.route('/messages/<id>', methods=["GET"])
def get_message(id):
    print('hi')
    message = Message.get_message(id)
    print(message)
    if message:
        return jsonify(message), 200
    return jsonify({'error': 'Message with id: {id} was not found.'}), 404

@main.route('/messages/<id>', methods=['PUT'])
def update_message(id):
    data = request.json
    data['edited'] = True
    data['updateAt'] = datetime.datetime.now()
    updated_message = Message.update_message(id, data)

    if updated_message.modified_count:
        return jsonify({'message': f'Message with id: {id} was updated'}), 200
    return jsonify({'message': f'Message with id: {id} was not updated'})