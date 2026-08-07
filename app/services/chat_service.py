"""
Chat Service
==============
Handles persistence and retrieval of chat messages.
"""

from app.extensions import db
from app.models.chat_history import ChatHistory


class ChatService:
    """Business logic for chat message persistence."""

    @staticmethod
    def save_message(user_id: int, role: str, content: str) -> ChatHistory:
        msg = ChatHistory(user_id=user_id, role=role, content=content)
        db.session.add(msg)
        db.session.commit()
        return msg

    @staticmethod
    def get_history(user_id: int, limit: int = 50) -> list[dict]:
        messages = (
            ChatHistory.query
            .filter_by(user_id=user_id)
            .order_by(ChatHistory.timestamp.asc())
            .limit(limit)
            .all()
        )
        return [m.to_dict() for m in messages]
