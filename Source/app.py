# Flask dependencies
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

# Initialize the application.
app = Flask(__name__)
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)

# Initialize SQL Alchemy
db = SQLAlchemy(app)

# Initialize Flask_Login
login_manager = LoginManager()
login_manager.init_app(app)

# Local dependencies
from controllers import *

# Run app
if __name__ == "__main__":
    app.run()

# Onthouden

# 1. Wel werken met verschillende routes display/samsung-galaxy etc
# 2. Forms checking, lengte/soort/wel of geen input etc! Met specifiek framework (wtf forms) of zelf
# 3. Begrijp hier alles van: http://flask-sqlalchemy.pocoo.org/2.3/
# 4. Opmerkingen bij alles zetten
