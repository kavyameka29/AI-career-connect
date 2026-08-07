"""
Database Service
----------------
Encapsulates all direct database operations so that routes stay thin.
"""

from datetime import datetime, timezone
from app.extensions import db
from app.models import Conversation, Message, User


def create_conversation(user_id: int = 1, title: str = "New Conversation", category: str = "general") -> int:
    """Create a new conversation and return its ID."""
    convo = Conversation(user_id=user_id, title=title, category=category)
    db.session.add(convo)
    db.session.commit()
    return convo.id


def save_message(conversation_id: int, role: str, content: str) -> Message:
    """Persist a single message to the database."""
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.session.add(msg)
    db.session.commit()
    return msg


def get_conversation_history(conversation_id: int) -> list[dict]:
    """Return all messages in a conversation, ordered chronologically."""
    messages = (
        Message.query
        .filter_by(conversation_id=conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    return [{"role": m.role, "content": m.content} for m in messages]


def get_dashboard_stats() -> dict:
    """Aggregate statistics for the dashboard."""
    total_users = User.query.count()
    total_conversations = Conversation.query.count()
    total_messages = Message.query.count()

    # Conversations by category
    categories = (
        db.session.query(Conversation.category, db.func.count(Conversation.id))
        .group_by(Conversation.category)
        .all()
    )

    # Recent conversations
    recent = (
        Conversation.query
        .order_by(Conversation.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "total_users": total_users,
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "categories": {cat: count for cat, count in categories},
        "recent_conversations": [
            {
                "id": c.id,
                "title": c.title,
                "category": c.category,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in recent
        ],
    }
