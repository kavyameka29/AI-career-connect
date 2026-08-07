"""
Resume Routes — Upload resume text and get AI-powered suggestions.
"""

from flask import Blueprint, request, jsonify, render_template
from app.services.ai_service import get_resume_suggestions

resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/")
def resume_page():
    """Render the resume review page."""
    return render_template("resume.html")


@resume_bp.route("/analyze", methods=["POST"])
def analyze_resume():
    """Accept resume text and return AI improvement suggestions."""
    data = request.get_json()
    resume_text = data.get("resume_text", "")

    if not resume_text.strip():
        return jsonify({"error": "Resume text cannot be empty"}), 400

    suggestions = get_resume_suggestions(resume_text)

    return jsonify({"suggestions": suggestions})
