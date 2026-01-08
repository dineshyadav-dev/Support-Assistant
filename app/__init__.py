from flask import Flask
from config import Config
from app.extensions import db,jwt, migrate


def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)


    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


 # Health check
    @app.route("/health")
    def health():
        return {"status": "ok", "message": "Support Assistant backend running"}


    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
