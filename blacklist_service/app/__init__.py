from flask import Flask
from flask_restful import Api
from flask_jwt_extended import create_access_token
from config import Config
from .extensions import db, ma, jwt
from .models import db
from .routes import register_routes
from . import models  # Para asegurar que SQLAlchemy registre los modelos


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    ma.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # token = create_access_token(identity="prueba@example.com")
        # app.config["STATIC_JWT_TOKEN"] = token  # 🔐 Guardamos el token generado
        # print(f"\n🔑 TOKEN DE PRUEBA:\nBearer {token}\n")

    api = Api(app)
    register_routes(api)
  

    return app

app = create_app()