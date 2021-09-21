from logging import debug
from flask import Flask, render_template 

app = Flask(__name__) 

@app.route("/")
def index():
    return render_template("one.html")
    # templates --> one.html
    # templates --> html --> one.html 
    # render_template("html/one.html")

app.run(debug=True)