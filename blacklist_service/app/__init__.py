from flask import Flask
from .models import db
from .routes import register_routes

def create_app(config_class=None):
    app = Flask(__name__)

    # Si recibe una clase de configuración, la aplica
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_pyfile("../config.py")

    db.init_app(app)

    from flask_restful import Api
    api = Api(app)
    register_routes(api)

    return app