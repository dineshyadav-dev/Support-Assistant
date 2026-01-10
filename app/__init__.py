from flask import Flask
from config import Config
from app.extensions import db,jwt, migrate
import os

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "uploads", "tickets")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    #app registration by using Blueprint
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from app.tickets.routes import ticket_bp
    app.register_blueprint(ticket_bp)

    return app
