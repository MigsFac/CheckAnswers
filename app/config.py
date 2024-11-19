import os
from dotenv import load_dotenv


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not set")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if os.getenv("FLASK_ENV") == "production":
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    else:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = (
            f"sqlite:///{os.path.join(BASE_DIR,'database','IntegrationDB.db')}"
        )
        # SQLALCHEMY_DATABASE_URI = "sqlite:///app/database/IntegrationDB.db"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
