from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
import os

#creates instance of flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Database configuration
# Defaults to local SQLite so the app runs without MySQL.
# Set DATABASE_URL to use MySQL, e.g.
# mysql+pymysql://flaskuser:flaskpass123@localhost/scheduling_db
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///scheduling.db",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise the databse
db = SQLAlchemy(app)

# databse table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable = False)

# Mock pending tasks for dashboard preview
MOCK_PENDING_TASKS = [
    {"title": "Follow up with client about Monday booking", "priority": "High"},
    {"title": "Prepare weekly team schedule", "priority": "Medium"},
    {"title": "Review clock-in discrepancies for Friday", "priority": "Low"},
    {"title": "Update meeting notes in shared workspace", "priority": "Medium"},
]

#root url, when '/' is accessed 
@app.route("/")
def index():
    current_user = None

    if "user_id" in session:
        current_user = User.query.get(session["user_id"])

    return render_template(
        "home.html",
        current_user=current_user,
        pending_tasks=MOCK_PENDING_TASKS,
        error=None,
        username="",
        email="",
    )

#Login and stay logged in, log in, create user
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"].strip()
    email = request.form["email"].strip()

    #find exisiting user with email
    user = User.query.filter_by(email=email).first()
    if user:
        if user.username != username:
            return render_template(
                "home.html",
                current_user=None,
                pending_tasks=MOCK_PENDING_TASKS,
                error="This user already exists. Username does not match this email.",
                username=username,
                email=email,
            )
        
        session["user_id"] = user.id
        session["username"] = user.username
        session["email"] = user.email
        return redirect(url_for("index"))
    try:
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["username"] = new_user.username
        session["email"] = new_user.email

        return redirect(url_for("index"))
    except IntegrityError:
        db.session.rollback()
        return render_template(
            "home.html",
            current_user=None,
            pending_tasks=MOCK_PENDING_TASKS,
            error="This user already exists. Please use a different username or email.",
            username=username,
            email=email,
        )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creates all tables in mySQL
    app.run(debug=True)
