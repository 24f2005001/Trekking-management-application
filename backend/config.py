import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "trek-super-secret-key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///mad2.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USER')
    MAIL_PASSWORD = os.getenv('MAIL_PASS')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USER')

    # flask caching (redis)

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/1')
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 1
    CACHE_DEFAULT_TIMEOUT = 60


    # celery config
    CELERY_BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_TIMEZONE = 'Asia/Kolkata'

        
