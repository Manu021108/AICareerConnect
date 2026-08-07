"""Chat history model — persists AI conversation threads."""

from datetime import datetime, timezone
from app.extensions import db


class ChatHistory(db.Model):
    """Stores individual messages in a conversation with the AI."""
    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "user" | "assistant"
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {"role": self.role, "content": self.content}

    def __repr__(self):
        return f"<ChatHistory id={self.id} role={self.role}>"
