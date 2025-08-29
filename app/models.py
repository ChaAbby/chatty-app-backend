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
    def get_user(id):
        return mongo.db.users.find_one({'_id': ObjectId(id)})
    
    @staticmethod
    def get_by_username(username):
        return mongo.db.users.find_one({'username': username})

    @staticmethod
    def update(id, new_email):
        return mongo.db.users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'email': new_email}}
        )
    
    @staticmethod
    def delete(id):
        # chats = Chat.get_by_user_id(id)
        # for chat in chats:
        #     pass
        #     # remove user from chats
        return mongo.db.users.delete_onf({'_id': ObjectId(id)})
    
class Chat:
    @staticmethod
    def create(name: Optional[str], ownerId, isGroup, members, createdAt, active):
        objectid_members = []
        for m in members:
            objectid_members.append(ObjectId(m))
        chat = {
              "name": name,
              "ownerId": ownerId,
              "isGroup": isGroup,       
             "members": objectid_members,  
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
    def modify_fields(id,data):
        update_operation = {}
        if data:
            update_operation['$set'] = data

            return mongo.db.chats.update_one({"_id": ObjectId(id)}, update_operation)

    @staticmethod
    def delete_members(id, members):
        if members:
            deleted_mems = []
            for m in members:
                deleted_mems.append(ObjectId(m))
            return mongo.db.chats.update_one({'_id': ObjectId(id)},{
                '$pull': {
                    'members':
                    {'$in': deleted_mems}
                    }
                }
            )     
    
    @staticmethod
    def add_members(id, members):
        if members:
            added_mems = []
            for m in members:
                added_mems.append(ObjectId(m))
            return mongo.db.chats.update_one({'_id': ObjectId(id)},{
                '$addToSet': {
                    'members':
                    {'$each': added_mems}
                    }
                }
            ) 

    @staticmethod
    def delete(id):
        return mongo.db.chats.delete_one({"_id": ObjectId(id)})
