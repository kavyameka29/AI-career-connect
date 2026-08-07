"""
Basic smoke tests for the Flask application.
"""

import pytest
from app import create_app


@pytest.fixture
def client():
    """Create a test client using the testing configuration."""
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Landing page should return 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_chat_page(client):
    """Chat page should return 200."""
    response = client.get("/chat/")
    assert response.status_code == 200


def test_dashboard_page(client):
    """Dashboard page should return 200."""
    response = client.get("/dashboard/")
    assert response.status_code == 200
