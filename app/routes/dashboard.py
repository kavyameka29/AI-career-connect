"""
Dashboard Routes — Dynamic analytics dashboard.
"""

from flask import Blueprint, jsonify, render_template
from app.services.db_service import get_dashboard_stats

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard_page():
    """Render the dashboard page."""
    return render_template("dashboard.html")


@dashboard_bp.route("/stats")
def dashboard_stats():
    """Return JSON stats for the dynamic dashboard (charts, counters)."""
    stats = get_dashboard_stats()
    return jsonify(stats)
