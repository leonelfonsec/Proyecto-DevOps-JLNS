from flask import Flask
from flask_restful import Api
from flask_jwt_extended import create_access_token
from app.extensions import db, ma, jwt
from app.models import db
from app.routes import register_routes
from app import models
from config import Config
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

def create_app(config_class=None):
    application = Flask(__name__)
    #application.config.from_object(Config)

    if config_class:
        application.config.from_object(config_class)
    else:
        application.config.from_object(Config)

    jwt.init_app(application)
    ma.init_app(application)
    db.init_app(application)

    if not application.config.get("TESTING", False):
        with application.app_context():
            db.create_all()
        # token = create_access_token(identity="prueba@example.com")
        # app.config["STATIC_JWT_TOKEN"] = token  # 🔐 Guardamos el token generado
        # print(f"\n🔑 TOKEN DE PRUEBA:\nBearer {token}\n")

    api = Api(application)
    register_routes(api)
  

    return application

application = create_app()
#print(f"\n🔗 DATABASE URI en runtime: {application.config['SQLALCHEMY_DATABASE_URI']}\n")

# if __name__ == "__main__":
#     application.run(host="0.0.0.0", port=5000)