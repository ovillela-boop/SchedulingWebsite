from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Shift, User
from datetime import datetime

shifts_bp = Blueprint("shifts", __name__)

@shifts_bp.route("/shifts")
def shifts_view():
    shifts = Shift.query.all()
    return render_template("shifts.html", shifts=shifts)

@shifts_bp.route("/shifts/<int:id>")
def shift_detail(id):
    shift = shift.query.get_or_404(id)
    return render_template("shift_detail.html", shift=shift)

@shifts_bp.route("/shifts/create", methods=["GET","POST"])
def create_shift():
    users=User.query.all()

    if request.method == "POST":
        user_id = request.form["user_id"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        start_time = datetime.strptime(request.form["start_time"], "%H:%M").time()
        end_time = datetime.strptime(request.form["end_time"], "%H:%M").time()
        notes = request.form.get("notes", "")

        new_shift = Shift(
            user_id=user_id,
            date=date,
            start_time=start_time,
            end_time=end_time,
            notes=notes
        )

        db.session.add(new_shift)
        db.session.commit()

        return redirect(url_for("shifts.shifts_view"))

    return render_template("create_shift.html", users=users)