"""Main routes — landing page and public-facing views."""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the landing / home page."""
    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Render the about page."""
    return render_template("about.html")
