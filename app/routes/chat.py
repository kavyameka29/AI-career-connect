"""
Chat Routes — AI career chat powered by Mistral API.
"""

from flask import Blueprint, request, jsonify, render_template
from app.services.ai_service import get_career_response
from app.services.db_service import save_message, get_conversation_history, create_conversation

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/")
def chat_page():
    """Render the chat interface."""
    return render_template("chat.html")


@chat_bp.route("/send", methods=["POST"])
def send_message():
    """Send a user message and get an AI response."""
    data = request.get_json()
    user_message = data.get("message", "")
    conversation_id = data.get("conversation_id")

    if not user_message.strip():
        return jsonify({"error": "Message cannot be empty"}), 400

    # Create a new conversation if none provided
    if not conversation_id:
        conversation_id = create_conversation(title=user_message[:50])

    # Save user message
    save_message(conversation_id, role="user", content=user_message)

    # Get conversation history for context
    history = get_conversation_history(conversation_id)

    # Call Mistral API
    ai_response = get_career_response(history)

    # Save assistant message
    save_message(conversation_id, role="assistant", content=ai_response)

    return jsonify({
        "response": ai_response,
        "conversation_id": conversation_id,
    })


@chat_bp.route("/history/<int:conversation_id>")
def get_history(conversation_id):
    """Retrieve full conversation history."""
    history = get_conversation_history(conversation_id)
    return jsonify({"messages": history})
