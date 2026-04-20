from flask import Blueprint, render_template

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
def tasks_view():
    return "<h1>Tasks page coming soon</h1>"