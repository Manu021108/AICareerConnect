"""AI Chat routes — Mistral-powered conversational career advisor."""

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.mistral_service import MistralService
from app.services.chat_service import ChatService

ai_chat_bp = Blueprint("ai_chat", __name__)


@ai_chat_bp.route("/send", methods=["POST"])
@login_required
def send_message():
    """Accept a user message, query Mistral, persist both, return the reply."""
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    # Persist user message
    ChatService.save_message(current_user.id, "user", user_message)

    # Build conversation context
    history = ChatService.get_history(current_user.id, limit=20)

    # Query Mistral
    reply = MistralService.get_career_advice(user_message, history)

    # Persist assistant reply
    ChatService.save_message(current_user.id, "assistant", reply)

    return jsonify({"reply": reply})


@ai_chat_bp.route("/history")
@login_required
def get_history():
    """Return the user's conversation history."""
    history = ChatService.get_history(current_user.id)
    return jsonify({"messages": history})
