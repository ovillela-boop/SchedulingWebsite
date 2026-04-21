from flask import Blueprint, render_template
from app.models import Task

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
def tasks_view():
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)