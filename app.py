"""Main Application"""
import os

import pytest
from flask.cli import FlaskGroup
from flask_migrate import Migrate

from apps import create_app, db
from apps.api import blueprint

app = create_app(os.getenv("FLASK_ENV", "default"))
app.register_blueprint(blueprint)

migrate = Migrate(app, db)
cli = FlaskGroup(app)


@cli.command("test")
def test():
    """Runs the unit tests."""
    pytest.main(args=["-v", "tests"])


if __name__ == "__main__":
    cli()
