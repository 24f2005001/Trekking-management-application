from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash
import redis
from flask_caching import Cache

from config import Config
from models import User
from db import db
from routes import register_routes
from cache import cache
import tasks
from tasks import init_celery
from celery.schedules import crontab



app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

jwt = JWTManager(app) 


db.init_app(app)

cache.init_app(app)


tasks.celery = tasks.init_celery(app)
celery_app = tasks.celery 

celery_app.conf.beat_schedule = {
    'daily-trek-reminders': {
        'task': 'tasks.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    'monthly-admin-report': {
        'task': 'tasks.send_monthly_report',
        'schedule': crontab(day_of_month=1, hour=8, minute=30),
    },
}





register_routes(app)

with app.app_context():
    db.create_all()

    admin = User.query.filter_by(email="admin@gmail.com").first()
    if not admin:
        admin = User(
            username="admin",
            email="admin@gmail.com",
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
