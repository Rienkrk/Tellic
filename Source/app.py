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

# Sorry Stijn; maar dit moest er even uit (punt 1)
# @app.route("/post", methods=['GET', 'POST'])
# def post():
#     if request.method == "GET":
#         db = connection.cursor()
#         existingPost = db.execute("SELECT title, text FROM posts WHERE id=1")
#         connection.commit()
#         existingPost = existingPost.fetchone()
#
#         return render_template("post.html", post=existingPost)
#     else:
#         reply = request.form.get("reply")
#         db = connection.cursor()
#         db.execute("INSERT INTO replies (user_id, post_id, phone_id, text) VALUES(?, ?, ?, ?)", (1, 1, 1, reply))
#         connection.commit()
#         flash('Uw antwoord is geplaatst!', 'alert-success')
#         return redirect(url_for("index"))
