# Contains authorization related pieces that include Register, login and logout
# Also contains helper functions

from flask import Blueprint, render_template, request, redirect, url_for, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User

auth_bp = Blueprint("auth", __name__)

#Helper Functions
def is_logged_in():
    return "user_id" in session

#Helper Function
def current_logged_in_user():
    if "user_id" in session:
        return db.session.get(User, session["user_id"])
    return None

#Helper Function
def is_manager():
    user = current_logged_in_user()
    return user is not None and user.role == "Manager"

# Mock pending tasks for dashboard preview
MOCK_PENDING_TASKS = [
    {"title": "Follow up with client about Monday booking", "priority": "High"},
    {"title": "Prepare weekly team schedule", "priority": "Medium"},
    {"title": "Review clock-in discrepancies for Friday", "priority": "Low"},
    {"title": "Update meeting notes in shared workspace", "priority": "Medium"},
]

@auth_bp.route("/register", methods=["POST"])
def register():
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()

    existing_user = User.query.filter(
        or_(User.name == username, User.email == email)
    ).first()

    if existing_user:
        return render_template(
            "home.html",
            current_user=None,
            pending_tasks=MOCK_PENDING_TASKS,
            error="Username or email already exists",
            username=username,
            email=email,
        )

    try:
        new_user = User(
            name = username,
            email = email,
            password_hash = generate_password_hash(password),
            role="Manager"
        )
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["name"] = new_user.name
        session["email"] = new_user.email
        session["role"] = new_user.role

        return redirect(url_for("main.dashboard"))

    except IntegrityError:
        db.session.rollback()
        return render_template(
            "home.html",
            current_user=None,
            pending_tasks=MOCK_PENDING_TASKS,
            error="Could not create account. Try again.",
            username=username,
            email=email
        )

@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form["email"].strip()
    password = request.form["password"].strip()

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["name"] = user.name
        session["email"] = user.email
        session["role"] = user.role
        return redirect(url_for("main.dashboard"))

    return render_template(
        "home.html",
        current_user=None,
        pending_tasks=MOCK_PENDING_TASKS,
        error="Invalid email or password",
        username="",
        email=email
    )

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))