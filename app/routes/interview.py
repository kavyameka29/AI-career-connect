"""
Interview Routes — Generate mock interview questions via AI.
"""

from flask import Blueprint, request, jsonify, render_template
from app.services.ai_service import get_interview_questions

interview_bp = Blueprint("interview", __name__)


@interview_bp.route("/")
def interview_page():
    """Render the interview prep page."""
    return render_template("interview.html")


@interview_bp.route("/generate", methods=["POST"])
def generate_questions():
    """Generate interview questions for a given job role."""
    data = request.get_json()
    job_role = data.get("job_role", "")
    difficulty = data.get("difficulty", "medium")

    if not job_role.strip():
        return jsonify({"error": "Job role is required"}), 400

    questions = get_interview_questions(job_role, difficulty)

    return jsonify({"questions": questions})
