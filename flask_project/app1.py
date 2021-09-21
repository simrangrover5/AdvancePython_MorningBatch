from logging import debug
from flask import Flask 

app = Flask(__name__)   # Flask --> class, app --> object 
# __name__ --> namespace --> __main__
# Flask("flask_project")

# route(path) --> decorator --> app 
@app.route("/")  # / --> localhost (domain), example.com --> /
def index():
    return "hello world"

@app.route("/home/")  # localhost/home/
def home():
    return "<h1 style='color:blue'>This is my home of python</h1>"

@app.route("/home/<name>/<int:age>/")
def showname(name, age):
    if age>=18:
        return f"""<h2 style='color:coral'>Welcome {name.upper()}. You can vote...</h2>"""
    return f"""<h2 style='color:coral'>Welcome {name.upper()}. You cannot vote...</h2>"""

app.run(host='localhost', port=80, debug=True)
# error --> show on front end debug = True

# localhost/home/simran --> Welcome Simran
# localhost/home/mansi --> Welcome Mansi
# localhost/home/shivangi --> Welcome Shivangi
# localhost/home/anyname
# localhost/home/<var>/ --> var --> variable (value be anything)
# var --> str, <int:var>, <float:var>