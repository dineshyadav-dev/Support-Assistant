from app.extensions import db
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__="users"

    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password_hash=db.Column(db.String(256), nullable=False)
    role=db.Column(db.String(20), nullable=False, default="USER")  # ADMIN, AGENT, USER
    created_at=db.Column(db.DateTime, server_default=db.func.now())


    def set_password(self,password):
        self.password_hash=generate_password_hash(password)            #it generate hash password and return to services

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)       #it check the password in db &give result to login service

