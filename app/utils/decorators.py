"""Reusable decorators — rate limiting, role checks, etc."""

from functools import wraps
from flask import abort
from flask_login import current_user


def role_required(role):
    """Restrict a route to users with a specific role."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or getattr(current_user, "role", None) != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
