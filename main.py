from flask import Flask, render_template

#creates instance of flask app
app = Flask(__name__)

#root url, when '/' is accessed 
@app.route("/")
def index():
    return render_template("index.html")
#When user visits the website
def home():
    return "Scheduling Webstie Loading..."

if __name__ == '__main__':
    app.run(debug=True)
