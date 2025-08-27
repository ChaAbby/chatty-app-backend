from . import mongo
from bson.objectid import ObjectId
from typing import Optional 

class User:
    @staticmethod
    def create(username, email, password, date, avatarUrl, role):
        user = {
            'username': username,
            'email': email,
            "password": password,
            "role": role,
            "lastSeen": date,
            "avatarUrl": avatarUrl

        }
        mongo.db.users.insert_one(user)
        return user

    @staticmethod
    def get_by_username(username):
        return mongo.db.users.find_one({'username': username})

    @staticmethod
    def update(username, new_email):
        mongo.db.users.update_one(
            {'username': username},
            {'$set': {'email': new_email}}
        )

    @staticmethod
    def delete(username):
        mongo.db.users.delete_one({'username': username})

class Chat:
    @staticmethod
    def create(name: Optional[str], ownerId, isGroup, members, createdAt, active):
        chat = {
              "name": name,
              "ownerId": ownerId,
              "isGroup": isGroup,       
             "members": members,  
              "createdAt": createdAt,
              "active": active,
        }
        mongo.db.chats.insert_one(chat)
        return chat
    @staticmethod
    def get_by_id(id):
        # Get all members data in all chats
        return mongo.db.chats.find_one({"_id": ObjectId(id)})

    @staticmethod
    def get_by_user_id(user_id):
        # Get all members data in all chats
        return mongo.db.chats.find({"members": int(user_id)})
