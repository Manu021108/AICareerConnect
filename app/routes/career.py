"""Career routes — profile management and skill assessment."""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.career_service import CareerService

career_bp = Blueprint("career", __name__)


@career_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Get or update the user's career profile."""
    if request.method == "POST":
        data = request.get_json()
        profile = CareerService.update_profile(current_user.id, data)
        return jsonify({"message": "Profile updated.", "profile_id": profile.id})

    profile = CareerService.get_profile(current_user.id)
    if not profile:
        return jsonify({"message": "No profile found."}), 404
    return jsonify(CareerService.profile_to_dict(profile))


@career_bp.route("/assess", methods=["POST"])
@login_required
def assess_skills():
    """Run an AI-driven skill assessment."""
    results = CareerService.run_assessment(current_user.id)
    return jsonify({"assessments": results})
