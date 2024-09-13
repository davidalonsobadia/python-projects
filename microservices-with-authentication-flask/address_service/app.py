# address_service/app.py
from .models import Address, User
from . import create_app, db, logger
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

app = create_app()

@app.route('/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    logger.debug('get_address Request')
    current_user_id = get_jwt_identity()
    existing_user = User.query.filter_by(username=current_user_id).first()
    if not existing_user:
        return jsonify({"message": "User not found"}), 400


    # Query all addresses belonging to the current user
    addresses = Address.query.filter_by(user_id=existing_user.id).all()

    # If no addresses found
    if not addresses:
        return jsonify({"message": "No addresses found for this user."}), 404

    # Convert addresses to a list of dictionaries
    address_list = [address.to_dict() for address in addresses]

    return jsonify({"addresses": address_list}), 200

# User creation endpoint
@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    logger.debug('create_user Request')
    data = request.get_json()

    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@app.route('/addresses', methods=['POST'])
@jwt_required()
def add_address():
    logger.debug('add_address Request')
    current_user_id = get_jwt_identity()
    
    data = request.get_json()

    user = User.query.filter_by(username=current_user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_address = Address(
        street=data.get('street'),
        city=data.get('city'),
        postal_code=data.get('postal_code'),
        user_id=user.id
    )
    
    db.session.add(new_address)
    db.session.commit()

    return jsonify({"message": "Address added successfully"}), 201