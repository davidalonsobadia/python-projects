from flask import Flask
from flask_restful import Api
from models import db
from config import Config
import commands
from resources import TasksListAPI, TasksAPI

# Create the Flask application and the Flask-RESTful API manager.
app = Flask(__name__)

app.config.from_object(Config)

# Initialize the Flask-SQLAlchemy object.
db.init_app(app)

# Create the Flask-RESTful API manager.
api = Api(app)
# Create the endpoints.
api.add_resource(TasksListAPI, '/tasks')
api.add_resource(TasksAPI, '/tasks/<int:task_id>')

commands.init_commands(app)

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables.
        db.create_all()
    # Start the Flask development web server.
    app.run(debug=True)
