from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

#creates instance of flask app
app = Flask(__name__)

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
    return render_template("home.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    email = request.form["email"]

    new_user = User(username=username, email=email)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("list_users"))
    
    except IntegrityError:
        db.sessiorn.rollback()
        return "Email already exists. Try a different one."

@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # creates all tables in mySQL
    app.run(debug=True)
