from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

#creates instance of flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

#mySQL configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://flaskuser:flaskpass123@localhost/scheduling_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise the databse
db = SQLAlchemy(app)

# databse table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable = False)


#root url, when '/' is accessed 
@app.route("/")
def index():
    current_user = None

    if "user_id" in session:
        current_user = User.query.get(session["user_id"])

    return render_template("home.html", current_user=current_user)

#Login and stay logged in, log in, create user
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    email = request.form["email"]

    #find exisiting user with email
    user = User.query.filter_by(email=email).first()
    if user:
        if user.username != username:
            return "Username does not match this email."
        
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
        db.session_rollback()
        return "Could not log in. Try again"
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
    




#Create user connected to mysql gathers username and email no password yet

# @app.route("/create_user", methods=["POST"])
# def create_user():
#     username = request.form["username"]
#     email = request.form["email"]

#     new_user = User(username=username, email=email)
    
#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for("list_users"))
    
#     except IntegrityError:
#         db.session.rollback()
#         return "Email already exists. Try a different one."

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creates all tables in mySQL
    app.run(debug=True)
