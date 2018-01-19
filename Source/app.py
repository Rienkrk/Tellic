from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3
from flask.ext.bcrypt import Bcrypt
# from fonAPI import FonApi

# Initialize the application.
app = Flask(__name__)
bcrypt = Bcrypt(app)
Session(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'jshd74hf8SDSD'
app.config['SECRET_KEY'] = 'jshd74hf8'

# Makes a connection with the database.
connection = sqlite3.connect("data.db", check_same_thread=False)

# Put application into debug mode, to disbale caching.
app.debug = True

@app.route("/registerHandler", methods=['GET', 'POST'])
def registerHandler():

    # Get user input via POST.
    username=request.form.get("username")
    password=request.form.get("password")
    passwordCheck=request.form.get("passwordCheck")

    # Check if passwords are the same.
    if password != passwordCheck:
        flash('Oops! Wachtwoorden komen niet overheen!', 'alert-danger')
        return render_template('register.html')

    # Hash and salt password
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")

    # Insert given data into database
    db = connection.cursor()
    db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, hashed))
    connection.commit()

    flash('U bent succesvol geregistreerd!', 'alert-success')
    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/")
def index():

    # fon = FonApi('86a627624640b46902d56f06fde28b703e638be64217e5fa')

    # phones = fon.getdevice('nokia 3210')

    return render_template("index.html")

if __name__ == "__main__":
    Session(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'jshd74hf8SDSD'
    app.run()

# if bcrypt.check_password_hash(hashed, password) == True:
#     return redirect(url_for("login"))
