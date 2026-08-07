"""Shared test fixtures."""

import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Create the Flask application for testing."""
    app = create_app("testing")
    yield app


@pytest.fixture(scope="function")
def db(app):
    """Provide a clean database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture
def client(app):
    """Provide a Flask test client."""
    return app.test_client()
