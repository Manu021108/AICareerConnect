"""Shared helper functions."""

import json


def safe_json_loads(data, default=None):
    """Parse JSON safely, returning a default on failure."""
    try:
        return json.loads(data) if data else default
    except (json.JSONDecodeError, TypeError):
        return default
