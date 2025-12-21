from flask import Flask
from .api.health_check import bp as health_check
from .api.auth import bp as auth
from .db.db import init_db
from flask_cors import CORS

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    with app.app_context():
        init_db()
    app.register_blueprint(health_check, url_prefix="/api")
    app.register_blueprint(auth, url_prefix="/api/auth")
    return app