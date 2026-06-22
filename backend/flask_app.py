import os
from flask import Flask, request
from flask_restful import Api, Resource
from flask_mail import Mail, Message
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

app = Flask(__name__)
api = Api(app)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USER')
mail = Mail(app)

#redis
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 1
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/1'
app.config['CACHE_DEFAULT_TIMEOUT'] = 60
cache = Cache(app)


# Celery Configuration

app.config['broker_url'] = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
app.config['result_backend'] = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')

celery = Celery(app.name, broker=app.config['broker_url'], backend=app.config['result_backend'])
celery.conf.broker_connection_retry_on_startup = True


# Celery Context Setup

def init_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config['broker_url'],
        backend=flask_app.config['result_backend']
    )
    celery_app.conf.update(flask_app.config)

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

celery = init_celery(app)

@celery.task(name="tasks.background_task") #change according to your ps
def background_task():
    return 'Background task completed'

@celery.task(name='tasks.daily_reminder')
def daily_reminder():
    employees=User.query.filter_by(role="employee") #change according to your ps
    return 'reminder sent'

class sendemail(Resource):
    @cache.cached(timeout=10)
    def get(self):
        email = "24f2005001@ds.study.iitm.ac.in"

        
        msg = Message(
            subject="Test Email from Flask",
            recipients=[email],  
            body="This is a test email sent via Flask and SMTP."
        )

        mail.send(msg)
        return {'msg': "mail send!"}

api.add_resource(sendemail, '/mail')

if __name__ == "__main__":
    app.run(debug=True)