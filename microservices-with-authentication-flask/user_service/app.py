from . import create_app, db, logger
from .models import UserProfile
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

app = create_app()

# Create user profile (only for authenticated users)
@app.route('/profiles', methods=['POST'])
@jwt_required()
def create_profile():
    logger.debug('register Request')
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    full_name = data.get('full_name')

    if not username or not email or not full_name:
        return jsonify({"error": "Missing required fields"}), 400

    new_user_profile = UserProfile(username=username, email=email, full_name=full_name)
    db.session.add(new_user_profile)
    db.session.commit()

    return jsonify({'message': 'Profile created successfully'}), 201

# Get user profile
@app.route('/profiles/<username>', methods=['GET'])
@jwt_required()
def get_profile(username):
    logger.debug('get_profile Request')
    current_user = get_jwt_identity()

    if current_user != username:
        return jsonify({'message': 'Unauthorized access'}), 403

    profile = UserProfile.query.filter_by(username=username).first()
    if not profile:
        return jsonify({'message': 'Profile not found'}), 404

    return jsonify({'username': profile.username, 'full_name': profile.full_name, 'email': profile.email}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
