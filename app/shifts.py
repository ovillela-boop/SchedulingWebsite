from flask import Blueprint

shifts_bp = Blueprint("shifts", __name__)

@shifts_bp.route("/shifts")
def shifts_view():
    return "<h1>Shifts page coming soon</h1>"