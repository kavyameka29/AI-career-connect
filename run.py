"""
Application Entry Point
-----------------------
Creates and runs the Flask application using the factory pattern.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
