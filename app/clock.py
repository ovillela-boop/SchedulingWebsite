from flask import Blueprint

clock_bp = Blueprint("clock", __name__)

@clock_bp.route("/clock")
def clock_view():
    return "<h1>Clock page coming soon</h1>"