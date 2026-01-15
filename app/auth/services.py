from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token,create_refresh_token
ALLOWED_ROLES={"ADMIN", "AGENT", "USER"}

def register_user_service(data):
    role = data.get("role", "USER").upper()
    if role not in ALLOWED_ROLES:
        return None, f"Invalid role. Allowed roles: {', '.join(ALLOWED_ROLES)}"

    if User.query.filter_by(email=data["email"]).first():
        return None, "User already exists"

    user = User(
        email=data["email"],
        role=data.get("role", "USER")
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()
    return user, None


def login_user_service(data):
    user = User.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return None, "Invalid credentials"

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    refresh_token=create_refresh_token(identity=str(user.id))
    return {
        "access_token": access_token,
        "refresh_token":refresh_token,
        "role": user.role
    }, None
