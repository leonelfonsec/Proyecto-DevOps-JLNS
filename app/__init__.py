from flask import Flask
from flask_restful import Api
from flask_jwt_extended import create_access_token
from config import Config
from .extensions import db, ma, jwt
from .models import db
from .routes import register_routes
from . import models  # Para asegurar que SQLAlchemy registre los modelos



