"""
Database Models
---------------
SQLAlchemy ORM models representing the application's data layer.
Each model maps to a SQLite table.
"""

from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    """Represents a platform user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    conversations = db.relationship("Conversation", backref="user", lazy=True)
    resumes = db.relationship("Resume", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Conversation(db.Model):
    """Stores a chat conversation (career Q&A, interview prep, etc.)."""

    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), default="New Conversation")
    category = db.Column(db.String(50), default="general")  # general | interview | resume
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    messages = db.relationship("Message", backref="conversation", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation {self.id}: {self.title}>"


class Message(db.Model):
    """A single message inside a conversation."""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id"), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Message {self.role}: {self.content[:30]}>"


class Resume(db.Model):
    """Stores uploaded resume text and AI suggestions."""

    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    original_text = db.Column(db.Text, nullable=False)
    suggestions = db.Column(db.Text)  # AI-generated suggestions (JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Resume {self.id} for User {self.user_id}>"
