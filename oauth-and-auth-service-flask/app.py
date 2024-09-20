import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

# Load the environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
print("Database path:", os.path.abspath('your_database.db'))


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)
