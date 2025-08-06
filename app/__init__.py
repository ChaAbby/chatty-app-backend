from flask import Flask
from flask_pymongo import PyMongo
from .config import Config
import certifi

# create PyMongo instance at module level
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app,tlsCAFile=certifi.where())


    from .routes import main
    app.register_blueprint(main)

    return app
