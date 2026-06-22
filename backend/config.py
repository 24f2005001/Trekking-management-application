import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "trek-super-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///mad2.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    