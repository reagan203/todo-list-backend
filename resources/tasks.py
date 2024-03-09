from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, TaskModel

class Tasks(Resource):
    def get(self):
        """Get all tasks."""
        # Retrieve all tasks from the database
        tasks = TaskModel.query.all()
        # Convert tasks to JSON format and return with HTTP status 200
        return jsonify([task.to_json() for task in tasks]), 200

    @jwt_required()
    def post(self):
        """Create a new task."""
        # Get JSON data from the request
        data = request.json
        # Check if request body is empty
        if not data:
            return {'error': 'Invalid JSON data in request body'}, 400

        # Extract task details from the JSON data
        title = data.get('title')
        # Check if the 'title' field is present
        if not title:
            return {'error': 'Title is required'}, 400

        # Get the current user's ID from the JWT token
        user_id = get_jwt_identity()
        # Create a new task object
        new_task = TaskModel(title=title,
                             description=data.get('description'),
                             priority=data.get('priority', 'medium'),
                             status=data.get('status', 'pending'),
                             user_id=user_id)
        # Add the new task to the database
        db.session.add(new_task)
        db.session.commit()
        # Return the newly created task in JSON format with HTTP status 201 (Created)
        return new_task.to_json(), 201

class Task(Resource):
    @jwt_required()
    def get(self, task_id):
        """Get a single task by ID."""
        # Get the current user's ID from the JWT token
        current_user_id = get_jwt_identity()
        # Query the task from the database by ID and user ID
        task = TaskModel.query.filter_by(id=task_id, user_id=current_user_id).first()
        # Check if the task exists and the current user is its owner
        if task:
            # Return the task details in JSON format with HTTP status 200 (OK)
            return task.to_json(), 200
        # Return an error message if the task is not found or unauthorized with HTTP status 404 (Not Found)
        return {'error': 'Task not found or unauthorized'}, 404

    @jwt_required()
    def put(self, task_id):
        """Update a task by ID."""
        # Get the current user's ID from the JWT token
        current_user_id = get_jwt_identity()
        # Query the task from the database by ID and user ID
        task = TaskModel.query.filter_by(id=task_id, user_id=current_user_id).first()
        # Check if the task exists and the current user is its owner
        if not task:
            # Return an error message if the task is not found or unauthorized with HTTP status 404 (Not Found)
            return {'error': 'Task not found or unauthorized'}, 404

        # Get JSON data from the request
        data = request.json
        # Check if request body is empty
        if not data:
            return {'error': 'Invalid JSON data in request body'}, 400

        # Update task attributes if provided in the request
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)

        # Commit the changes to the database
        db.session.commit()
        # Return the updated task details in JSON format with HTTP status 200 (OK)
        return task.to_json(), 200

    @jwt_required()
    def delete(self, task_id):
        """Delete a task by ID."""
        # Get the current user's ID from the JWT token
        current_user_id = get_jwt_identity()
        # Query the task from the database by ID and user ID
        task = TaskModel.query.filter_by(id=task_id, user_id=current_user_id).first()
        # Check if the task exists and the current user is its owner
        if not task:
            # Return an error message if the task is not found or unauthorized with HTTP status 404 (Not Found)
            return {'error': 'Task not found or unauthorized'}, 404

        # Delete the task from the database
        db.session.delete(task)
        db.session.commit()
        # Return a success message with HTTP status 200 (OK)
        return {'message': 'Task deleted successfully'}, 200
