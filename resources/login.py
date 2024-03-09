from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models import UserModel

class Login(Resource):
    def post(self):
        # Retrieve JSON data from the request body
        data = request.json
        
        # Check if request body is empty or if 'email' or 'password' keys are missing
        if data is None or 'email' not in data or 'password' not in data:
            return {'error': 'Email and password are required'}, 400

        # Extract email and password from the JSON data
        email = data['email']
        password = data['password']

        # Query the database for a user with the provided email
        user = UserModel.query.filter_by(email=email).first()

        # Check if the user exists and if the provided password is correct
        if not user or not user.check_password(password):
            return {'error': 'Invalid email or password'}, 401

        # Generate an access token for the authenticated user
        access_token = create_access_token(identity=user.id)

        # Create the Authorization header containing the access token
        auth_header = f"Bearer {access_token}"

        # Return the access token along with the Authorization header
        return {'access_token': access_token, 'Authorization': auth_header,'message':'login succesful'}, 200
