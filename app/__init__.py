from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
import os
from .views import *
from .initdb import create_Title
from app.config import DevConfig, ProdConfig


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    environment = os.getenv("FLASK_ENV", "development")
    if environment == "production":
        load_dotenv(".env.production")
    else:
        load_dotenv(".env")

    app = Flask(__name__)

    if environment == "production":
        app.config.from_object("config.ProdConfig")
    else:
        app.config.from_object("config.DevConfig")

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(views.main)

    return app
