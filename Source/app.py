from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3
from flask_bcrypt import Bcrypt
from tempfile import mkdtemp
# from fonAPI import FonApi

import sys
import json
import requests

class FonApi:

    __ApiUrl = 'https://fonoapi.freshpixl.com/v1/'

    def __init__(self, apikey, url=None):

        self.__ApiUrl = FonApi.__ApiUrl

        if url is not None:
            self.__ApiUrl = url

        self.__ApiKey = apikey

    def getdevice(self, device, position=None, brand=None):
        """
            Get device data object and return a json list
        :param device:
        :param position:
        :param brand:
        :return device list:
        """
        url = self.__ApiUrl + 'getdevice'
        postdata = {'brand': brand,
                    'device': device,
                    'position': position,
                    'token': self.__ApiKey}
        headers = {'content-type': 'application/json'}
        result = self.sendpostdata(url, postdata, headers)
        try:
            return result.json()
        except AttributeError:
            return result

    def sendpostdata(self, url, postdata, headers, result = None):
        """
            Send data to the server
        :param url:
        :param postdata:
        :param headers:
        :return requests.post result:
        """
        try:
            result = requests.post(url, data=json.dumps(postdata), headers=headers)

            # Consider any status other than 2xx an error
            if not result.status_code // 100 == 2:
                return "Error status page: " + str(result)
            # Try send the result text else send the error
            try:
                if result.json()['status'] == 'error':

                    if result.json()['message'] == 'Invalid Token. Generate a Token at fonoapi.freshpixl.com.':
                        return "Check __ApiKey"

                return result.json()['message']
            except:
                pass

            return result
        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            return "Connect error. Check URL"


# Initialize the application.
app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Session(app)
# app.config["SESSION_FILE_DIR"] = mkdtemp()
# app.secret_key = 'jshd74hf8SDSD'
# app.config['SECRET_KEY'] = 'jshd74hf8SDSD'

# Makes a connection with the database.
connection = sqlite3.connect("data.db", check_same_thread=False)

# Put application into debug mode, to disable caching.
app.debug = True

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/loginHandler", methods=['GET', 'POST'])
def loginHandler():
    username=request.form.get("username").lower()
    password=request.form.get("password")

    # Check if everything is filled in.
    if not password or not username:
        flash('Oops! Vul alstublieft uw gebruikersnaam en wachtwoord in!', 'alert-danger')
        return render_template('register.html')

	# Receive
    db = connection.cursor()
    user = db.execute("SELECT * FROM users WHERE username=?", (username, ))
    connection.commit()
    user = user.fetchone()

	# Check if the username exists.
    if user is None:
        flash("Oops! U heeft een verkeerd wachtwoord of gerbuikersnaam opgegeven!", 'alert-danger')
        return redirect(url_for("login"))

    # Check if the password given by the user is correct.
    if bcrypt.check_password_hash(user[2], password) == True:
        flash("U bent succesvol ingelogd " + username + "!", 'alert-success')
        session["user"] = {'id': user[0], 'username': user[1]}
        return redirect(url_for("index"))
    else:
        flash("Oops! U heeft een verkeerd wachtwoord of gebruikersnaam opgegeven!", 'alert-danger')
        return redirect(url_for("login"))

@app.route("/registerHandler", methods=['GET', 'POST'])
def registerHandler():

    # Get user input via POST.
    username=request.form.get("username").lower()
    password=request.form.get("password")
    passwordCheck=request.form.get("passwordCheck")

    # Check if everything is filled in.
    if not password or not username:
        flash('Oops! Vul alstublieft uw gebruikersnaam en wachtwoord in!', 'alert-danger')
        return render_template('register.html')

    # Make sure the user has a unique username.
    db = connection.cursor()
    sql = db.execute("SELECT username FROM users WHERE username=?", (username, ))
    connection.commit()
    sql = sql.fetchone()

    if sql is not None:
        flash("Helaas! Uw gebruikersnaam is helaas al in gebruik!", 'alert-warning')
        return render_template('register.html')

    # Check if passwords are the same.
    if password != passwordCheck:
        flash('Oops! Wachtwoorden komen niet overheen!', 'alert-danger')
        return render_template('register.html')

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
    session["user"] = {'id': db.lastrowid, 'username': username}

    flash('U bent succesvol geregistreerd ' + username + "!",  'alert-success')

    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/post", methods=['GET', 'POST'])
def post():
    if request.method == "GET":
        db = connection.cursor()
        existingPost = db.execute("SELECT title, text FROM posts WHERE id=1")
        connection.commit()
        existingPost = existingPost.fetchone()

        return render_template("post.html", post=existingPost)
    else:
        reply = request.form.get("reply")
        db = connection.cursor()
        db.execute("INSERT INTO replies (user_id, post_id, phone_id, text) VALUES(?, ?, ?, ?)", (1, 1, 1, reply))
        connection.commit()
        flash('Uw antwoord is geplaatst!', 'alert-success')
        return redirect(url_for("index"))
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/display")
def display():
    if request.method == "GET":

        # Uses the token to get into the API.
        fon = FonApi('3618ac67ea1695322d52be3bca323ac4eb29caca9570dbe5')

        # Get all the information about a specific phone and return the html file.
        phonesVar = fon.getdevice('samsung galaxy s7')
        return render_template("display.html", phones=phonesVar)

@app.route("/")
def index():

    # Get all posts from database, most recent first.

    db = connection.cursor()
    posts = db.execute("SELECT * FROM posts ORDER BY timestamp DESC")
    connection.commit()
    posts = posts.fetchall()

    # Get favorites from user.
    db = connection.cursor()
    favorites = db.execute("SELECT * FROM favorites WHERE user_id = 233")
    connection.commit()
    favorites = favorites.fetchall()


    return render_template("index.html", posts=posts, favorites=favorites)


@app.route("/createPost", methods=['GET', 'POST'])
def createPost():
    if request.method == "POST":

        # Get written post via POST.
        title = request.form.get("title")
        post = request.form.get("post")

        # Add post to database.
        db = connection.cursor()
        db.execute("INSERT INTO posts (username, title, text) VALUES(?, ?, ?)", (session.get('user')['username'], title, post))
        connection.commit()
        flash('Uw post is geplaatst!', 'alert-success')
        return redirect(url_for("index"))

    else:
        return render_template("createPost.html")

if __name__ == "__main__":
    Session(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'jshd74hf8SDSD'
    app.config['SECRET_KEY'] = 'jshd74hf8SDSD'
    app.run()
