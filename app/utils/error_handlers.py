"""Custom error handlers for the application."""

from flask import render_template, jsonify, request


def _wants_json():
    return request.accept_mimetypes.best == "application/json"


def handle_404(error):
    if _wants_json():
        return jsonify({"error": "Not found"}), 404
    return render_template("errors/404.html"), 404


def handle_403(error):
    if _wants_json():
        return jsonify({"error": "Forbidden"}), 403
    return render_template("errors/403.html"), 403


def handle_500(error):
    if _wants_json():
        return jsonify({"error": "Internal server error"}), 500
    return render_template("errors/500.html"), 500
