from flask import Blueprint, request
from app.auth.services import register_user_service, login_user_service
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token
from app.models.user import User

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


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    new_access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return {
        "access_token": new_access_token
    }, 200

