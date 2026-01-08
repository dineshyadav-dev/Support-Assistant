from flask import Blueprint, request
from app.extensions import db
from app.models.user import User
from flask_jwt_extended import create_access_token

auth_bp =Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('register',methods=['POST'])
def register():
    data=request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return {"message":"user already exist"},400
    user=User(
        email=data['email'],
        role=data.get('role','USER')
        )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return {"message":"user register successfully."},201


@auth_bp.route('login',methods=['POST'])
def login():
    data=request.get_json()
    user=User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return {"message":"Invalid credentials"},401

    token=create_access_token(identity={"id":user.id,"role":user.role})
    return {"access_token":token,"role":user.role}
