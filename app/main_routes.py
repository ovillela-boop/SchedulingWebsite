# Main routes that are used 

from flask import Blueprint, render_template, redirect, url_for, session
from .models import User
from .auth import current_logged_in_user, MOCK_PENDING_TASKS

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    current_user = current_logged_in_user()

    return render_template(
        "home.html",
        current_user=current_user,
        pending_tasks=MOCK_PENDING_TASKS,
        error=None,
        username="",
        email="",
    )

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("main.index"))
    return render_template("dashboard.html")

@main_bp.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)