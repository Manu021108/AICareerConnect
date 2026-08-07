"""Career profile model — stores user skills, goals, and preferences."""

from datetime import datetime, timezone
from app.extensions import db


class CareerProfile(db.Model):
    """Stores a user's career-related data for AI recommendations."""
    __tablename__ = "career_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    current_role = db.Column(db.String(150))
    desired_role = db.Column(db.String(150))
    skills = db.Column(db.Text)            # JSON-serialized list
    experience_years = db.Column(db.Integer, default=0)
    education = db.Column(db.String(250))
    interests = db.Column(db.Text)         # JSON-serialized list
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self):
        return f"<CareerProfile user_id={self.user_id}>"
