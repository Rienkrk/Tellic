from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3

# Initialize the application.
app = Flask(__name__)

# Makes a connection with the database.
connection = sqlite3.connect("data.db", check_same_thread=False)

# Put application into debug mode, to disbale caching.
app.debug = True

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/")
def index():

    db = connection.cursor()
    var1 = 'y'
    var2 = 'x'
    db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (var1, var2))
    connection.commit()

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
