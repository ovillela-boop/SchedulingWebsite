from flask import Flask
import os
from .models import db

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = "supersecretkey"

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///scheduling.db",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .auth import auth_bp
    from .main_routes import main_bp
    from .manager import manager_bp
    from .tasks import tasks_bp
    from .shifts import shifts_bp
    from .clock import clock_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(manager_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(shifts_bp)
    app.register_blueprint(clock_bp)

    return app