from . import mongo

class User:
    @staticmethod
    def create(username, email, password):
        user = {
            'username': username,
            'email': email,
            "password": password
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
