from flask import Blueprint, render_template, redirect, url_for
from .auth import is_logged_in, is_manager, current_logged_in_user

manager_bp = Blueprint("manager", __name__)

@manager_bp.route("/manager")
def manager_dashboard():
    if not is_logged_in():
        return redirect(url_for("main.index"))

    if not is_manager():
        return redirect(url_for("main.index"))

    return render_template("manager.html", current_user=current_logged_in_user())