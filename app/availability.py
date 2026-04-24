from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
from app.models import db, Availability

# Blueprint initialized
availability_bp = Blueprint("availability", __name__)

# Main page route, displays calendar
@availability_bp.route("/availability")
def availability_view():
    return render_template("availability.html")

# API route that send saved info to FullCalendat as JSON
@availability_bp.route("/availability/events")
def availability_events():

    # Get users id info
    user_id = session.get("user_id")

    # Only use users saved blocks
    blocks = Availability.query.filter_by(user_id=user_id).all()

    # Convert record into JSON format for FullCalendar
    events = []
    for block in blocks:
        events.append({
            "id": block.id,
            "title": block.status.capitalize(),
            "start": block.start_time.isoformat(),
            "end": block.end_time.isoformat(),
            #green for avaiable and red for busy
            "color": "#22c55e" if block.status == "available" else "#ef4444"
        })

    return jsonify(events)


#API route that received the new avail. blocks from the calendar
@availability_bp.route("/availability/create", methods=["POST"])
def create_availability():
    # Read JSON data sent from JS fetch()
    data = request.get_json()

    # New availabilty record created with users info
    block = Availability(
        user_id=session.get("user_id"),
        start_time=datetime.fromisoformat(data["start"]),
        end_time=datetime.fromisoformat(data["end"]),
        status=data["status"],
        notes=data.get("notes", "")
    )

    # Save the new block to the database
    db.session.add(block)
    db.session.commit()

    return jsonify({"success": True})