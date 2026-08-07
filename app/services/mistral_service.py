"""
Mistral AI Service
====================
Encapsulates all calls to the Mistral API. Every other module
talks to Mistral through this service — never directly.
"""

from flask import current_app
from mistralai import Mistral


SYSTEM_PROMPT = (
    "You are AICareerConnect, an expert AI career advisor. "
    "Help users explore career paths, identify skill gaps, "
    "prepare for interviews, and build learning roadmaps. "
    "Be encouraging, specific, and data-driven."
)


class MistralService:
    """Wrapper around the Mistral chat completions API."""

    @staticmethod
    def _get_client():
        api_key = current_app.config["MISTRAL_API_KEY"]
        return Mistral(api_key=api_key)

    @staticmethod
    def get_career_advice(user_message: str, history: list[dict] | None = None) -> str:
        """Send a message (with optional history) and return the assistant reply."""
        client = MistralService._get_client()
        model = current_app.config["MISTRAL_MODEL"]

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = client.chat.complete(model=model, messages=messages)
        return response.choices[0].message.content

    @staticmethod
    def assess_skill(skill_name: str, user_context: str) -> dict:
        """Ask Mistral to evaluate a specific skill and return score + tips."""
        client = MistralService._get_client()
        model = current_app.config["MISTRAL_MODEL"]

        prompt = (
            f"Evaluate the user's proficiency in '{skill_name}' based on the "
            f"following context:\n\n{user_context}\n\n"
            "Return a JSON object with keys: score (0-100), recommendation (string)."
        )

        response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {"score": 0, "recommendation": response.choices[0].message.content}
