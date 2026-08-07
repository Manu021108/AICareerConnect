"""
AICareerConnect - Flask Application Factory
============================================
Initializes the Flask app, registers blueprints, extensions,
and configures the application context.
"""

from flask import Flask
from app.extensions import db, migrate, cors, login_manager
from app.config import config_by_name


def create_app(config_name="development"):
    """Application factory pattern for Flask."""
    app = Flask(__name__,
                static_folder="../static",
                template_folder="../templates")

    # Load configuration
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    _register_extensions(app)

    # Register blueprints
    _register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    return app


def _register_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    login_manager.init_app(app)

    # Create database tables
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()


def _register_blueprints(app):
    """Register Flask blueprints."""
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.ai_chat import ai_chat_bp
    from app.routes.speech import speech_bp
    from app.routes.career import career_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(ai_chat_bp, url_prefix="/api/chat")
    app.register_blueprint(speech_bp, url_prefix="/api/speech")
    app.register_blueprint(career_bp, url_prefix="/api/career")


def _register_error_handlers(app):
    """Register custom error handlers."""
    from app.utils.error_handlers import (
        handle_404, handle_500, handle_403
    )
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    app.register_error_handler(403, handle_403)
