from flask import Flask
from flask_restful import Api
from flask_jwt_extended import create_access_token
from config import Config
from .extensions import db, ma, jwt  # ✅ Importa desde extensions
from .routes import register_routes
from . import models  # Asegura que los modelos se registren antes del create_all


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa las extensiones primero
    jwt.init_app(app)
    ma.init_app(app)
    db.init_app(app)

    # Ahora sí puedes usar create_all dentro de un contexto
    with app.app_context():
        db.create_all()
        token = create_access_token(identity="prueba@example.com")
        print(f"Token generado:\n{token}")

    api = Api(app)
    register_routes(api)

    return app

