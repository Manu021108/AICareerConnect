"""
Database Models Package
========================
Imports all models so SQLAlchemy discovers them during db.create_all().
"""

from app.models.user import User
from app.models.career_profile import CareerProfile
from app.models.chat_history import ChatHistory
from app.models.skill_assessment import SkillAssessment

__all__ = ["User", "CareerProfile", "ChatHistory", "SkillAssessment"]
