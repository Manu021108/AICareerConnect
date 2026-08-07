"""Dashboard routes — dynamic, data-driven user dashboard."""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.models.skill_assessment import SkillAssessment
from app.models.chat_history import ChatHistory

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def overview():
    """Render the main dashboard page."""
    return render_template("dashboard/overview.html")


@dashboard_bp.route("/api/stats")
@login_required
def stats():
    """Return JSON stats consumed by the dashboard charts."""
    assessments = SkillAssessment.query.filter_by(user_id=current_user.id).all()
    chat_count = ChatHistory.query.filter_by(user_id=current_user.id).count()

    skill_data = [
        {"skill": a.skill_name, "score": a.score}
        for a in assessments
    ]

    return jsonify({
        "total_chats": chat_count,
        "total_assessments": len(assessments),
        "skills": skill_data,
    })
