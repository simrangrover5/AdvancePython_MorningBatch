from logging import debug
from flask import Flask, render_template, request, redirect, url_for
import pymysql as sql 
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass
from passlib.hash import pbkdf2_sha256 as sha
from flask import make_response, session

email = None
name = None
passwd = None 
username = None

app = Flask(__name__)
app.secret_key = "oiohfoihoiehoihehfoihouheouhuofhhouhuohuohooiioj"

def connectivity():
    db = sql.connect(host='localhost', port=3306, user="root", password="", database="batch9am")
    cursor = db.cursor()
    return db, cursor 

@app.route("/")
def index():
    if request.cookies.get("islogin"):
        return render_template("afterlogin.html")
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/login/")
def login():
    if request.cookies.get("islogin"):
        return render_template("afterlogin.html")
    return render_template("login.html")
    
@app.route("/signup/")
def signup():
    return render_template("signup.html")

@app.route("/aftersignup/", methods=['GET', 'POST'])
def aftersignup():
    if request.method == 'GET':
        return redirect(url_for("signup"))  # url_for("view_name")
    else:
        global name, email, passwd, username
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
            msg = MIMEMultipart()
            msg['To'] = email
            msg['From'] = "simrangrover5@gmail.com"
            msg['Subject'] = "Email Verification Mail from MYSERVER"
            host = "smtp.gmail.com"

            html = """
            <html>
            <body>
            <h3 style='color:red'>Click on the link below to verify your email</h3>
            <a href='localhost/confirm/'>CLICK ON THIS</a>
            </body>"""

            p = MIMEText(html, "html")
            # creating a MIMEText object defining the type of content we are going to send 

            msg.attach(p)
            context = ssl.create_default_context()
            password = getpass("\n Password --> ")
            db.close()
            try:
                with smtplib.SMTP_SSL(host, 465, context=context) as server:
                    server.login(msg['From'], password)
                    server.sendmail(msg['From'], msg['To'], msg.as_string())
            except Exception as error:
                print(error)
                msg = "Please fill the details again"
                return render_template("signup.html", msg=msg)
            else:
                msg = "Please check your email."
                return render_template("signup.html", msg=msg)

        # return f"{name}, {email}, {passwd}"

@app.route("/afterlogin/", methods=['GET', 'POST'])
def afterlogin():
    if request.method == "GET":
        return redirect(url_for("login"))
    else:
        email = request.form.get("email")
        passwd = request.form.get("passwd")
        db, cursor = connectivity()
        cursor.execute(f"select * from users where email='{email}'")  
        data = cursor.fetchone()
        db.close()
        if data:
            if sha.verify(passwd, data[2]):
                # resp = make_response(render_template("afterlogin.html"))
                # resp.set_cookie('email', email)
                # resp.set_cookie('islogin', 'True')
                # return resp 
                session['email'] = email
                session['islogin'] = 'true'
                return render_template("afterlogin.html")
            else:
                msg = "Invalid Password"
                return render_template("login.html", msg=msg)
        else:
            msg = "Invalid Email"
            return render_template("login.html", msg=msg)

@app.route("/confirm/")
def confirm():
    global name, email, passwd, username 
    db, cursor = connectivity()
    passwd = sha.hash(passwd)
    cmd = f"insert into users values('{name}', '{email}', '{passwd}', '{username}')"
    cursor.execute(cmd)
    db.commit()
    msg = "Successfully Registered"
    return render_template("login.html", msg = msg)

@app.route("/logout/")
def logout():
    # resp = make_response(render_template("index.html"))
    # resp.delete_cookie('email')
    # resp.delete_cookie("islogin")
    # return resp 
    del session['email']
    del session['islogin']
    return redirect(url_for("index"))

app.run(host='localhost', port=80, debug=True)

# simrangrover5@gmail.com --> username --> simrangrover5
# password validation --> atleast 8 characters, num, special char, upper and lower alphabets
# session cookies 