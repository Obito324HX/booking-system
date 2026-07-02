import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///booking.db"
    ).replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from app.models import models  # noqa: F401  (registers models with SQLAlchemy)
    from app.routes.businesses import businesses_bp
    from app.routes.services import services_bp
    from app.routes.bookings import bookings_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(businesses_bp, url_prefix="/api/businesses")
    app.register_blueprint(services_bp, url_prefix="/api")
    app.register_blueprint(bookings_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
