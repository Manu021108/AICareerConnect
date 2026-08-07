"""
Career Service
================
Handles career profile management and AI-driven skill assessments.
"""

import json
from app.extensions import db
from app.models.career_profile import CareerProfile
from app.models.skill_assessment import SkillAssessment
from app.services.mistral_service import MistralService


class CareerService:
    """Business logic for career profiles and assessments."""

    @staticmethod
    def get_profile(user_id: int) -> CareerProfile | None:
        return CareerProfile.query.filter_by(user_id=user_id).first()

    @staticmethod
    def update_profile(user_id: int, data: dict) -> CareerProfile:
        profile = CareerProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            profile = CareerProfile(user_id=user_id)
            db.session.add(profile)

        profile.current_role = data.get("current_role", profile.current_role)
        profile.desired_role = data.get("desired_role", profile.desired_role)
        profile.skills = json.dumps(data.get("skills", []))
        profile.experience_years = data.get("experience_years", profile.experience_years)
        profile.education = data.get("education", profile.education)
        profile.interests = json.dumps(data.get("interests", []))

        db.session.commit()
        return profile

    @staticmethod
    def profile_to_dict(profile: CareerProfile) -> dict:
        return {
            "current_role": profile.current_role,
            "desired_role": profile.desired_role,
            "skills": json.loads(profile.skills) if profile.skills else [],
            "experience_years": profile.experience_years,
            "education": profile.education,
            "interests": json.loads(profile.interests) if profile.interests else [],
        }

    @staticmethod
    def run_assessment(user_id: int) -> list[dict]:
        """Evaluate each skill in the user's profile using Mistral."""
        profile = CareerService.get_profile(user_id)
        if not profile or not profile.skills:
            return []

        skills = json.loads(profile.skills)
        context = f"Role: {profile.current_role}, Experience: {profile.experience_years} years"
        results = []

        for skill in skills:
            evaluation = MistralService.assess_skill(skill, context)
            assessment = SkillAssessment(
                user_id=user_id,
                skill_name=skill,
                score=evaluation.get("score", 0),
                recommendation=evaluation.get("recommendation", ""),
            )
            db.session.add(assessment)
            results.append({
                "skill": skill,
                "score": assessment.score,
                "recommendation": assessment.recommendation,
            })

        db.session.commit()
        return results
