from logging import debug
from flask import Flask, render_template 

app = Flask(__name__) 

@app.route("/")
def index():
    return render_template("one.html")
    # templates --> one.html
    # templates --> html --> one.html 
    # render_template("html/one.html")

@app.route("/home/<name>/")
def home(name):
    return render_template("one.html", n = name)

@app.route("/<name>/<city>/<state>/")
def show(name, city, state):
    data = {
        'Name': name,
        "City": city,
        "State": state
    }
    return render_template("one.html", data=data)
    

app.run(debug=True)