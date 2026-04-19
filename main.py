from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
import os
from functools import wraps

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

# Initialize the db with app
from models import db, User, Task, Shift, ClockLog, Booking
db.init_app(app)

#Helper Functions
def is_logged_in():
    return "user_id" in session
#Helper Function
def current_logged_in_user():
    if "user_id" in session:
        return db.session.get(User, session["user_id"])
    return None
#Helper Function
def is_manager():
    user = current_logged_in_user()
    return user is not None and user.role == "Manager"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_manager():
            return redirect(url_for('tasks_view'))
        return f(*args, **kwargs)
    return decorated_function

#root url, when '/' is accessed 
@app.route("/")
def index():
    current_user = current_logged_in_user()
    pending_tasks = []
    
    if current_user:
        if current_user.role == "Manager":
            pending_tasks = Task.query.filter(Task.status != 'completed').limit(5).all()
        else:
            pending_tasks = Task.query.filter_by(assigned_to=current_user.id).filter(Task.status != 'completed').limit(5).all()

    return render_template(
        "home.html",
        current_user=current_user,
        pending_tasks=pending_tasks,
        error=None,
        name="",
        email="",
    )

#Protecting pages behind login using dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html")

# a new user must register before using login 
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"].strip()
    email = request.form["email"].strip()
    password = request.form["password"].strip()

    existing_user = User.query.filter(
        or_(User.name == username, User.email == email)
    ).first()

    if existing_user:
        return render_template(
            "home.html",
            current_user=None,
            pending_tasks=[],
            error="Username or email already exists",
            name=username,
            email=email,
        )
    
    try:
        new_user = User(
            name = username,
            email = email,
            password_hash = generate_password_hash(password),
            #temporary all new users as manager until fully configured
            role="Manager"
        )
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["name"] = new_user.name
        session["email"] = new_user.email

        return redirect(url_for("index"))
    
    except IntegrityError:
        db.session.rollback()
        return render_template(
            "home.html",
            current_user=None,
            pending_tasks=[],
            error="Could not create account. Try again.",
            name=username,
            email=email
        )
 
#Login after user has created account (logged in)
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"].strip()
    password = request.form["password"].strip()

    #find exisiting user with email
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["name"] = user.name
        session["email"] = user.email
        return redirect(url_for("index"))
    
    return render_template(
        "home.html",
        current_user=None,
        pending_tasks=[],
        error="Invalid email or password",
        name="",
        email=email
    )

# Manager Dashboard (anyone not manager role gets redirected)
@app.route("/manager")
def manager_dashboard():
    if not is_logged_in():
        return redirect(url_for("index"))
    
    if not is_manager():
        return redirect(url_for("index"))
    
    return render_template("manager.html", current_user=current_logged_in_user())

# Log out on top right corner
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# temporary webpage that shows all current users
@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/tasks")
@login_required
def tasks_view():
    user = current_logged_in_user()
    if user.role == "Manager":
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(assigned_to=user.id).all()
        
    users_list = User.query.all() if user.role == "Manager" else []
    return render_template("tasks.html", tasks=tasks, current_user=user, users=users_list)

@app.route("/tasks/create", methods=["GET", "POST"])
@login_required
@manager_required
def create_task():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        assigned_to_id = request.form.get("assigned_to")
        
        new_task = Task(
            title=title,
            description=description,
            assigned_to=int(assigned_to_id) if assigned_to_id else None,
            created_by=session["user_id"]
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('tasks_view'))
        
    users_list = User.query.all()
    return render_template("create_task.html", users=users_list, current_user=current_logged_in_user())

@app.route("/tasks/<int:id>/complete", methods=["POST"])
@login_required
def complete_task(id):
    task = Task.query.get_or_404(id)
    user = current_logged_in_user()
    
    if user.role == "Manager" or task.assigned_to == user.id:
        task.status = "completed"
        db.session.commit()
        
    return redirect(url_for('tasks_view'))

@app.route("/tasks/<int:id>/update", methods=["POST"])
@login_required
@manager_required
def update_task(id):
    task = Task.query.get_or_404(id)
    
    status = request.form.get("status")
    assigned_to = request.form.get("assigned_to")
    
    if status in ['pending', 'in_progress', 'completed']:
        task.status = status
    if assigned_to:
        task.assigned_to = int(assigned_to)
        
    db.session.commit()
    return redirect(url_for('tasks_view'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creates all tables in mySQL
    app.run(debug=True)
