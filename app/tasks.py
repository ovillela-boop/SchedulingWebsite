from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from app.models import db, Task, User

tasks_bp = Blueprint("tasks", __name__)

@tasks_bp.route("/tasks")
def tasks_view():
    tasks = Task.query.all()
    return render_template("tasks.html", tasks=tasks)

@tasks_bp.route("/tasks/create", methods=["GET", "POST"])
def create_task():
    users = User.query.all()

    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        assigned_to = request.form.get("assigned_to")
        due_date_raw = request.form.get("due_date")

        due_date = None
        if due_date_raw:
            due_date = datetime.strptime(due_date_raw, "%Y-%m-%d")

        created_by = session.get("user_id")

        new_task = Task(
            title=title,
            description=description,
            assigned_to=int(assigned_to) if assigned_to else None,
            created_by=created_by,
            due_date=due_date
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("tasks.tasks_view"))

    return render_template("create_task.html", users=users)

@tasks_bp.route("/tasks/<int:id>/complete", methods=["POST"])
def complete_task(id):
    task =Task.query.get_or_404(id)
    task.status = "completed"
    db.session_commit()
    return redirect(url_for("tasks.tasks_view"))

@tasks_bp.route("/tasks/<int:id>/update", methods=["POST"])
def update_task(id):
    task = Task.query.get_or_404(id)

    task.status = request.form.get("status")
    assinged_to = request.form.get("assigned_to")
    task.assigned_to = int(assinged_to) if assigned_to else None

    db.session.commit()
    return redirect(url_for("tasks.tasks_view"))
