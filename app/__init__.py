"""
Application Factory
-------------------
Initializes the Flask app, registers extensions (SQLAlchemy, Migrate),
and attaches all blueprints. Using the factory pattern allows creating
multiple app instances (useful for testing).
"""

from flask import Flask
from config import config_by_name
from app.extensions import db, migrate
import os


def create_app(config_name: str = "development") -> Flask:
    """Create and configure the Flask application."""

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    # Load configuration
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Ensure instance and upload directories exist
    os.makedirs(app.config.get("UPLOAD_FOLDER", "instance/uploads"), exist_ok=True)
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.chat import chat_bp
    from app.routes.resume import resume_bp
    from app.routes.interview import interview_bp
    from app.routes.speech import speech_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(resume_bp, url_prefix="/resume")
    app.register_blueprint(interview_bp, url_prefix="/interview")
    app.register_blueprint(speech_bp, url_prefix="/speech")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    # Create database tables on first request
    with app.app_context():
        from app import models  # noqa: F401 — ensures models are registered
        db.create_all()

    return app
