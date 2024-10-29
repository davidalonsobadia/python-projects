from flask_restful import Resource
from flask import request, make_response
from models import Task, db

class TasksListAPI(Resource):
    def get(self):
        # Get all the tasks from the database.
        tasks = Task.query.all()
        # Convert the tasks to JSON and return a response.
        task_list = [{'id': task.id, 'description': task.description} for task in tasks]
        return {'tasks': task_list}

    def post(self):
        # Get the JSON data from the request.
        task_data = request.get_json()
        # Check if the data is valid.
        if not task_data:
            return {'message': 'No input data provided'}, 400
        description = task_data.get('description')
        if not description:
            return {'message': 'Description is required'}, 400
        # Add the task to the database.
        new_task = Task(description=description)
        db.session.add(new_task)
        # Commit the task to the database.
        db.session.commit()
        # Return a message to the user.
        return {'message': 'Task added', 'task': {'id': new_task.id, 'description': new_task.description}}


class TasksAPI(Resource):
    def put(self, task_id):
        task_update_data = request.get_json()
        if not task_update_data:
            return {'message': 'No input data provided'}, 400
        description = task_update_data.get('description')
        if not description:
            return {'message': 'Description is required'}, 400

        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return {'message': 'Task not found'}, 404
        
        task.description = task_update_data.get('description')

        db.session.add(task)
        db.session.commit()

        return {'id': task.id, 'description': task.description}
    
    def get(self, task_id):
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return {'message': 'Task not found'}, 404
        
        return {'id': task.id, 'description': task.description}
    
    def delete(self, task_id):
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return {'message': 'Task not found'}, 404
        
        db.session.delete(task)
        db.session.commit()

        response = make_response('')
        response.status_code = 200
        return response
