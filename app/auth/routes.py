from flask import Blueprint, request
from app.auth.services import register_user_service, login_user_service

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user, error = register_user_service(data)

    if error:
        return {"message": error}, 400

    return {"message": "User registered successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    result, error = login_user_service(data)

    if error:
        return {"message": error}, 401

    return result, 200
