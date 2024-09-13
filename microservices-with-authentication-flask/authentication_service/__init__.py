import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

logging.basicConfig(level=logging.DEBUG)  # or use logging.INFO, logging.ERROR based on your needs
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    return app
