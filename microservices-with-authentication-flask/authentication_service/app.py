import requests
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import create_app, db, logger

app = create_app()

JWT_SECRET = app.config['SECRET_KEY']

# Registration, login, and delete endpoints
@app.route('/register', methods=['POST'])
def register():
    logger.debug('register Request')
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    password_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Create JWT token for the new user
    access_token = create_access_token(identity=username)

    user_service_url = 'http://user_service:5002/profiles'
    user_data = {
        "username": data['username'],
        "email": data['email'],
        "full_name": data['full_name']
    }
    user_service_response = send_post_request(user_service_url, user_data, access_token)
    logger.info(user_service_response)
    if user_service_response.status_code != 201:
        return jsonify({"message": "Failed to create user in user_service"}), 500

    # Add the user in address_service
    address_service_url = 'http://address_service:5003/users'
    address_service_data = {
        "username": data['username']
    }
    address_service_response = send_post_request(address_service_url, address_service_data, access_token)

    if address_service_response.status_code != 201:
        return jsonify({"message": "Failed to create user in address_service"}), 500

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    logger.debug('login Request')
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Helper function to send a POST request with a JWT token
def send_post_request(service_url, data, token):
    logger.debug('send_post_request Request')
    headers = {
        'Authorization': f'Bearer {token}',  # Include the JWT token in the header
        'Content-Type': 'application/json'   # Set content type to JSON
    }
    try:
        logger.info(service_url)
        logger.info(data)
        logger.info(token)
        response = requests.post(service_url, json=data, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while making request to {service_url}: {e}")
        return None