from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3


connection = sqlite3.connect("data.db", check_same_thread=False)
app = Flask(__name__)

app.debug = True

@app.route("/")
def index():

    db = connection.cursor()
    var1 = 'y'
    var2 = 'x'
    db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (var1, var2))
    connection.commit()

    test = 'testsss2'
    return render_template("index.html", test=test)

if __name__ == "__main__":
    app.run()
