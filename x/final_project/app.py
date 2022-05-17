from crypt import methods
from distutils.log import error
import os
from platform import java_ver
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def error(error, code=400):  
    return render_template("error.html", code=code, error=error)

#global variables
GENDERS = ["Male", "Female"]


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///messanger.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def messages():
    friends = db.execute("SELECT id, name, email FROM users WHERE id IN (SELECT user2 FROM friends WHERE user1 = ?)", session["user_id"])
    id = session["user_id"]
    return render_template("index.html", friends=friends, id=id)




@app.route("/dialogue")
def dialogue():
    id = request.args.get("id")
    if id:
        dialogue = db.execute("SELECT sender_id, receiver_id, message, timestamp FROM messages WHERE sender_id = ? AND receiver_id = ? OR receiver_id = ? AND sender_id = ?", session["user_id"], id, session["user_id"], id)
    return jsonify(dialogue)

@app.route("/send")
def send():
    r = request.args.get("r")
    m = request.args.get("m")
    if m:
        db.execute("INSERT INTO messages (sender_id, receiver_id, message, timestamp) VALUES (?, ?, ?, ?)", session["user_id"], r, m, datetime.now())
        dialogue = db.execute("SELECT sender_id, receiver_id, message, timestamp FROM messages WHERE sender_id = ? OR receiver_id = ?", session["user_id"], session["user_id"])

    return jsonify(dialogue)



@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":

        #getting input
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.execute("SELECT * FROM users WHERE email = ?", email)

        #ckecking for email and password
        if len(user) != 1 or not check_password_hash(user[0]["password"], password):
            return error("User doesn't exist or password isn't correct")

        session["user_id"] = user[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        #checking email
        email = request.form.get("email")
        if (len(db.execute("SELECT * FROM users WHERE email = ?", email)) != 0) or not email:
            return error("Email already exists")
        
        #checking password
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        if (password != confirm) or len(password) < 6:
            return error("Password is incorrect")
        hash = generate_password_hash(password)
        
        #inserting into db
        date = datetime.now()
        id = db.execute("INSERT INTO users (email, password, reg_date) VALUES (?, ?, ?)", email, hash, date)
        session["user_id"] = id

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    if request.method == "POST":
        #validating name form
        new_name = request.form.get("new_name")
        if new_name:
            db.execute("UPDATE users SET name = ? WHERE id = ?", new_name, session["user_id"])

        #validating email form
        new_email = request.form.get("new_email")
        if new_email:
            email = db.execute("SELECT email FROM users WHERE email = ?", new_email)
            if len(email) != 0:
                return error("Email exists")
            db.execute("UPDATE users SET email = ? WHERE id = ?", new_email, session["user_id"])

        #validating phone form
        new_phone = request.form.get("new_phone")
        if new_phone:
            if len(new_phone) > 15 or len(new_phone) < 5:
                return error("Phone is incorrect")
            db.execute("UPDATE users SET phone = ? WHERE id = ?", new_phone, session["user_id"])

        #validating sex form
        new_sex = request.form.get("new_sex")
        if new_sex in GENDERS:
            db.execute("UPDATE users SET sex = ? WHERE id = ?", new_sex, session["user_id"])

        #validating password form
        old_password = request.form.get("old_password")
        if old_password:
            password = db.execute("SELECT password FROM users WHERE id = ?", session["user_id"])[0]["password"]
            if not check_password_hash(password, old_password):
                return error("Old password is incorrect")
        new_password = request.form.get("new_password")
        if new_password:
            if len(new_password) < 6:
                return error("Password is too short")
            hash = generate_password_hash(new_password)
            db.execute("UPDATE users SET password = ? WHERE id = ?", hash, session["user_id"])
        return redirect("/profile")
    
    else:
        profile = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        email = profile[0]["email"]
        name = profile[0]["name"]
        reg = profile[0]["reg_date"]
        sex = profile[0]["sex"]
        phone = profile[0]["phone"]
        return render_template("profile.html", email=email, name=name, reg=reg, sex=sex, phone=phone, genders=GENDERS)

@app.route("/contacts", methods=["POST", "GET"])
@login_required
def contacts():
    if request.method == "GET":
        friends = db.execute("SELECT id, name, phone, email FROM users WHERE id IN (SELECT user2 FROM friends WHERE user1 = ?)", session["user_id"])
        return render_template("contacts.html", friends=friends)
    else:
        id_user2 = request.form.get("id")
        if id_user2 != None:
            check = db.execute("SELECT * FROM friends WHERE user1 = ? AND user2 = ?", session["user_id"], id_user2)
            if len(check) == 0:
                if session["user_id"] == id_user2:
                    return error("You cannot add yourself to you friends")
                db.execute("INSERT INTO friends (user1, user2) VALUES (?, ?)", session["user_id"], id_user2)
                return redirect("/contacts")
            else:
                return redirect("/contacts")

        id_friend = request.form.get("id_friend")
        if id_friend != None:
            db.execute("DELETE FROM friends WHERE user1 = ? AND user2 = ?", session["user_id"], id_friend)
            return redirect("/contacts")
        return error("Not correct ID")


@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        people = db.execute("SELECT id, name, email, sex, phone  FROM users WHERE email LIKE ? OR name LIKE ? OR phone LIKE ?", q + "%", q + "%", q + "%")
    else:
        people = []
    return jsonify(people)

