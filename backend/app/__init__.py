from flask import Flask
from .api.health_check import bp as health_check
from .api.auth import bp as auth
from .routes.locations import bp as locations_bp
from .routes.sensors import bp as sensors_bp
from flask_cors import CORS
from app.db.db import close_db

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.teardown_appcontext(close_db)

    app.register_blueprint(health_check, url_prefix="/api")
    app.register_blueprint(auth, url_prefix="/api/auth")
    # Register locations and sensors under explicit API subpaths
    app.register_blueprint(locations_bp, url_prefix="/api/locations")
    app.register_blueprint(sensors_bp, url_prefix="/api/sensors")

    return app