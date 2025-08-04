from flask_pymongo import PyMongo
from flask import Flask
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI']= os.getenv("DB_URI")
mongo = PyMongo(app)
db = mongo.chatty_db

collection = db.users

