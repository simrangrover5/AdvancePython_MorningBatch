from logging import debug
from flask import Flask, render_template, request, redirect, url_for
import pymysql as sql 

app = Flask(__name__)

def connectivity():
    db = sql.connect(host='localhost', port=3306, user="root", password="", database="batch9am")
    cursor = db.cursor()
    return db, cursor 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/login/")
def login():
    return render_template("login.html")
    
@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/aftersignup/", methods=['GET', 'POST'])
def aftersignup():
    if request.method == 'GET':
        return redirect(url_for("signup"))  # url_for("view_name")
    else:
        name = request.form.get("full_name")
        email = request.form.get("email")
        passwd = request.form.get("passwd")
        username = email.split("@")[0]
        db, cursor = connectivity()
        cursor.execute(f"select email from users where email='{email}'")  
        data = cursor.fetchall()
        if data:
            msg = "Email Already Exists"
            return render_template("login.html", msg=msg)
        else:
            cmd = f"insert into users values('{name}', '{email}', '{passwd}', '{username}')"
            cursor.execute(cmd)
            db.commit()
            msg = "Successfully Registered"
            return render_template("login.html", msg = msg)
        # return f"{name}, {email}, {passwd}"

@app.route("/afterlogin/", methods=['GET', 'POST'])
def afterlogin():
    if request.method == "GET":
        return redirect(url_for("login"))
    else:
        email = request.form.get("email")
        passwd = request.form.get("passwd")
        db, cursor = connectivity()
        cursor.execute(f"select email from users where email='{email}' and password='{passwd}'")  
        data = cursor.fetchall()
        if data:
            return "USER EXISTS"
        else:
            msg = "Invalid Email or Password"
            return render_template("login.html", msg=msg)

app.run(host='localhost', port=80, debug=True)

# simrangrover5@gmail.com --> username --> simrangrover5
# password validation --> atleast 8 characters, num, special char, upper and lower alphabets
# session cookies 