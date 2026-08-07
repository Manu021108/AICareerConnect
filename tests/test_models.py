"""Tests for User model."""

from app.models.user import User


def test_password_hashing(db):
    user = User(username="jane", email="jane@test.com")
    user.set_password("mypassword")

    assert user.check_password("mypassword") is True
    assert user.check_password("wrongpassword") is False


def test_user_repr(db):
    user = User(username="john", email="john@test.com")
    assert repr(user) == "<User john>"
