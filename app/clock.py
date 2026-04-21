from flask import Blueprint, render_template, redirect, url_for, session
from datetime import datetime, timezone
from app.models import db, ClockLog

clock_bp = Blueprint("clock", __name__)

@clock_bp.route("/clock")
def clock_view():
    user_id = session.get("user_id")

    if not user_id:
        return "No logged-in user found in session", 400

    last_log = (
        ClockLog.query
        .filter_by(user_id=user_id)
        .order_by(ClockLog.id.desc())
        .first()
    )

    if last_log and last_log.clock_in and not last_log.clock_out:
        current_status = "Clocked In"
    else:
        current_status = "Clocked Out"

    return render_template(
        "clock.html",
        current_status=current_status,
        last_log=last_log
    )


@clock_bp.route("/clock/in", methods=["POST"])
def clock_in():
    user_id = session.get("user_id")

    if not user_id:
        return "No logged-in user found in session", 400

    open_log = (
        ClockLog.query
        .filter_by(user_id=user_id, clock_out=None)
        .order_by(ClockLog.id.desc())
        .first()
    )

    if open_log:
        return redirect(url_for("clock.clock_view"))

    new_log = ClockLog(
        user_id=user_id,
        clock_in=datetime.now(timezone.utc)
    )

    db.session.add(new_log)
    db.session.commit()

    return redirect(url_for("clock.clock_view"))


@clock_bp.route("/clock/out", methods=["POST"])
def clock_out():
    user_id = session.get("user_id")

    if not user_id:
        return "No logged-in user found in session", 400

    open_log = (
        ClockLog.query
        .filter_by(user_id=user_id, clock_out=None)
        .order_by(ClockLog.id.desc())
        .first()
    )

    if open_log:
        open_log.clock_out = datetime.now(timezone.utc)
        db.session.commit()

    return redirect(url_for("clock.clock_view"))