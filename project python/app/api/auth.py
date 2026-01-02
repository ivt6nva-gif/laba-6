from flask import Blueprint, request, jsonify
from app.service.auth.auth import verify_user, users_by_user_name, generate_user
from app.schemas.auth import LoginRequest, RegistrationRequest
from pydantic import ValidationError

bp = Blueprint("auth", __name__)


@bp.post("/login")
def login():
    try:
        data = LoginRequest(**(request.get_json() or {}))
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    user = verify_user(data.username, data.password)

    if user is None:
        return jsonify({"error": "Wrong username or password"}), 401

    return jsonify({"data": user}), 200

@bp.post("/registration")
def register():
    try:
        data = RegistrationRequest(**(request.get_json() or {}))
    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400

    user = users_by_user_name(data.username)

    if user is not None:
        return jsonify({"error": "User already exists"}), 409

    new_user = generate_user(data.username, data.password)
    return jsonify({"data": new_user}), 201