from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
import sqlite3
from flask.ext.bcrypt import Bcrypt
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
    sql = db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, hashed))
    sql = db.execute("SELECT FROM users (username) VALUES(?)", (username, hashed))
    session["user"] = sql['username']
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

    fon = FonApi('3618ac67ea1695322d52be3bca323ac4eb29caca9570dbe5')

    phonesVar = fon.getdevice('oneplus 3t')

    return render_template("index.html", phones=phonesVar)

if __name__ == "__main__":
    Session(app)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'jshd74hf8SDSD'
    app.run()

# if bcrypt.check_password_hash(hashed, password) == True:
#     return redirect(url_for("login"))
