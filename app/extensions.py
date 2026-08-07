"""
Flask Extensions
----------------
All third-party Flask extensions are instantiated here (without an app)
so they can be imported anywhere and initialized later via init_app().
This avoids circular imports.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
