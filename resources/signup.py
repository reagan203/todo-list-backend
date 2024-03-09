from flask_restful import Resource
from models import db, UserModel
from flask import request
from flask_jwt_extended import create_access_token
from flask_mail import Message
from flask_mail import Mail
from app import mail

class Signup(Resource):
    def post(self):
        # Get JSON data from request
        data = request.json
        
        # Check if request body is empty
        if data is None:
            return {'error': 'Request body is empty'}, 400

        # Extract email and password from JSON data
        email = data.get('email')
        password = data.pop('password', None)  # Remove password from data

        # Check if the email is already registered
        if UserModel.query.filter_by(email=email).first():
            return {'error': 'Email is already registered'}, 400

        # Create a new user object
        user = UserModel(**data)

        # If password exists, hash it before saving
        if password:
            user.set_password(password)

        # Save the new user to the database
        db.session.add(user)
        db.session.commit()

        # Send welcome email
        send_welcome_email(email)

        # Generate access token using Flask-JWT-Extended
        access_token = create_access_token(identity=user.id)

        # Return response with access token
        return {'access_token': access_token}, 201

def send_welcome_email(email):
    # Create a welcome email message
    msg = Message('Welcome to our platform!', sender='reaganm746@gmail.com', recipients=[email])
    msg.body = "Thank you for signing up! We're excited to have you on board."

    # Send the email
    mail.send(msg)  
