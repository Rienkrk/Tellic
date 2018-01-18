from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
app = Flask(__name__)

app.debug = True
app.config['DEBUG'] = True

@app.route("/")
def index():
    test = 'test2'
    return render_template("index.html", test=test)

if __name__ == "__main__":
    app.run()
