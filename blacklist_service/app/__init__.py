from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from .routes import register_routes
from config import Config

ma = Marshmallow()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    ma.init_app(app)
    db.init_app(app)
    jwt.init_app(app)

    api = Api(app)
    register_routes(api)

    return app