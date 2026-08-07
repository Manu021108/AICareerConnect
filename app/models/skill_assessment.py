"""Skill assessment model — tracks AI-generated skill evaluations."""

from datetime import datetime, timezone
from app.extensions import db


class SkillAssessment(db.Model):
    """Stores the results of an AI-driven skill assessment."""
    __tablename__ = "skill_assessments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float, default=0.0)        # 0–100
    recommendation = db.Column(db.Text)
    assessed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<SkillAssessment {self.skill_name} score={self.score}>"
