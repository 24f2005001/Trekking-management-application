from flask import Flask

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from config import Config
from models import User
from db import db
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

jwt = JWTManager(app)   

db.init_app(app)


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