"""
Top level module

This module:

- Contains create_app()
- Registers extensions
"""

from flask import Flask

# Import config
from config import config_by_name

# Import extensions
from .extensions import bcrypt, db, login_manager


def create_app(config_name):
    """
    Flask app create method

    Args:
        config_name

    Returns:
        app
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    bcrypt.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    return app
