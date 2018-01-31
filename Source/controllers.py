from app import *
from models import *
from api import *
import requests
import json
from sqlalchemy import desc
from collections import Counter
from helpers import *

# Route for the index.
@app.route("/")
def index():

    # Get posts from database, most recent first.
    posts = Post.query.order_by(desc(Post.created_on)).all()

    # Get the 3 most popular phones.
    phones = Favorite.query.all()
    popular = Counter([phone.phone for phone in phones]).most_common(3)

    # Return the posts and most popular phones to the index view.
    return render_template("index.html", posts=posts, popular=popular)

# Route for searching in the search bar from navigation.
@app.route("/search", methods=['GET', 'POST'])
def search():
    searchInput = request.args['searchText']

    # Get the phones related to the given search input from the API.
    phones = fon.getdevice(searchInput)

    # Return a json dump to the jquery function in search.js
    return json.dumps({'phones':phones});

# Route for registering.
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:

        # Get the given user information.
        username=request.form.get("username").lower()
        password=request.form.get("password")
        passwordCheck=request.form.get("passwordCheck")

        # Check if everything is filled in. Return a message when not.
        if not password or not username or not passwordCheck:
            flash('Oops! Vul alstublieft uw gebruikersnaam en wachtwoord in!', 'alert-danger')
            return redirect(url_for("register"))

        # Check if passwords are the same. Return a message when not.
        elif password != passwordCheck:
            flash('Oops! Wachtwoorden komen niet overheen!', 'alert-danger')
            return render_template("register.html", username=username)

        # Check if username is already used. Return a message when not.
        elif User.query.filter_by(username=username).first():
            flash("Helaas! Uw gebruikersnaam is al in gebruik!", 'alert-warning')
            return render_template("register.html")

        # Make sure the username consists of only numbers and letters. Return a message when not.
        elif username.isalnum() == False:
            flash("Uw gebruikersnaam mag alleen bestaan uit letters en cijfers!", 'alert-warning')
            return render_template("register.html", username=username)

        # Make sure both username and password have a minimal and maximal length. Return a message when not.
        elif len(username) < 5 or len(username) > 15:
            flash("Uw gebruikersnaam dient tussen de 5 en 15 tekens lang zijn!", 'alert-warning')
            return render_template("register.html", username=username)
        elif len(password) < 5 or len(password) > 40:
            flash("Uw wachtwoord dient minimaal 5 tekens lang te zijn!", 'alert-warning')
            return render_template("register.html", username=username)

        # When every demand is met. Add the user to the database.
        else:

            # Hash and salt the password.
            hashedPassword = bcrypt.generate_password_hash(password).decode("utf-8")
            newUser = User(username, hashedPassword)
            db.session.add(newUser)
            db.session.commit()

            # Log the user in and add him to the database.
            login_user(newUser)

            # Tell the user he is succesfully logged in.
            flash("U bent succesvol geregistreerd " + username + "!", 'alert-success')
            return redirect(url_for("index"))

# Get the right user when the user is loaded (when logging in).
@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username = username).first()

# Route for logging in.
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:

        # Get the given login information.
        username=request.form.get("username").lower()
        password=request.form.get("password")

        # Check if both required login instances are given else return a error (message).
        if not password or not username:
            flash('Oops! Geef zowel een gebruikersnaam als een wachtwoord op!', 'alert-danger')
            return render_template("login.html", username=username)

        # Check if the given user is in the database. If not return a error (message).
        userInstance = User.query.filter_by(username=username).first()
        if not userInstance:
            flash('Oops! U heeft een verkeerd wachtwoord of gebruikersnaam opgegeven!', 'alert-danger')
            return render_template("login.html", username=username)

        # If the user is found in the database check his password.
        else:
            if bcrypt.check_password_hash(userInstance.password, password) == True:
                login_user(userInstance)
                flash("U bent succesvol ingelogd " + username + "!", 'alert-success')
                return redirect(url_for("index"))
            else:

                # If the passwords did not match give the user a error (message).
                flash('Oops! U heeft een verkeerd wachtwoord of gebruikersnaam opgegeven!', 'alert-danger')
                return redirect(url_for("login"))

# Logout the user and give the user a message that he was succesfully logged out.
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('U bent succesvol uitgelogd, tot ziens!', 'alert-success')
    return redirect(url_for("index"))

# Route for creating a post.
@app.route("/createPost", methods=['GET', 'POST'])
@login_required
def createPost():
    if request.method == "GET":
        return render_template("createPost.html")
    else:

        # Get given information via post.
        title = request.form.get("title")
        post = request.form.get("post")

        # Make sure the post has a title and has content, else return a warning.
        if not title:
            flash("Uw post moet een titel hebben!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)
        if len(post) == 0:
            flash("Uw post moet inhoud hebben!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)

        # Make sure the title and post does not exeed the maximum allowed lenght, else return a warning.
        if len(post) > 1500:
            flash("Uw post mag maximaal uit 1500 tekens bestaan!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)
        elif len(title) > 100:
            flash("Uw titel mag maximaal uit 100 tekens bestaan!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)

        # Add post to database.
        else:
            newPost = Post(current_user.id, title, post)
            db.session.add(newPost)
            db.session.commit()

            # Give the user a message that the post was succesfully created.
            flash('U heeft uw post succesvol aangemaakt!', 'alert-success')
            return redirect(url_for("index"))

# Route for all the users.
@app.route("/profiel/<username>")
@login_required
def profiel(username):

    # Get specific user.
    userInstance = User.query.with_entities(User.id).filter_by(username=username).first()

    # Get replies, posts and favorites of specific user.
    replies = Reply.query.filter_by(user_id=userInstance[0]).order_by(desc(Reply.created_on)).all()
    posts = Post.query.filter_by(user_id=userInstance[0]).order_by(desc(Post.created_on)).all()
    favorites = Favorite.query.filter_by(user_id=userInstance[0]).all()

    # Return the replies, posts and favorites to the view.
    return render_template("profiel.html", posts=posts, replies=replies, favorites=favorites)

# Route for a specific phone.
@app.route("/display/<phone>")
def display(phone):

    # Get a image from Qwant API
    image = Qwant.get_image(phone)

    # Get specifications from fonAPI
    phone = fon.getdevice(phone)

    # Return the image and phone information to the the view.
    return render_template("display.html", phone=phone, image=image)

# Route for replying to a post.
@app.route("/reply", methods=['GET', 'POST'])
def reply():
    # Get written reply via POST.
    reply = request.form.get("reply")
    post_id = request.form.get("post_id")
    phone = request.form.get("phone")

    # Make sure the reply is not longer than 1000 characters.
    if len(reply) > 1000:
        flash("Uw antwoord mag maximaal uit 1000 tekens bestaan!", 'alert-warning')
        return redirect("reply")

	# Add post to database.
    else:
        newReply = Reply(current_user.id, post_id, reply, phone)
        db.session.add(newReply)
        db.session.commit()

		# When a reply is made succesfully return a succes message.
        flash('U heeft uw reply succesvol aangemaakt!', 'alert-success')
        return redirect("post/" + post_id)

# Route for getting to a specific post.
@app.route("/post/<post_id>")
def post(post_id):
    if request.method == "GET":

        # Get given post.
        post = Post.query.filter_by(id=post_id).first()

        # Get replies of given post.
        replies = Reply.query.filter_by(post_id=post_id).order_by(desc(Reply.created_on)).all()

		# Return the replies and post to the view.
        return render_template("post.html", post=post, replies=replies)

# Route for adding a phone to your favorits.
@app.route("/favorite", methods=['GET', 'POST'])
def favorite():

    # Get phone name from hidden form.
    phone = request.form.get('phone')

	# Check if phone is not already in the user his favorites, if not return a warning message.
    if not Favorite.query.filter_by(user_id=current_user.id, phone=phone).first():

        # Add favorite to database.
        addFavorite = Favorite(current_user.id, phone)
        db.session.add(addFavorite)
        db.session.commit()

		# Return a message that the phone was succesfully addes.
        flash('Deze telefoon is toegevoegd aan uw favorieten!', 'alert-success')
    else:
        flash('Deze telefoon staat al in uw favorieten', 'alert-warning')
    return redirect("display/" + phone)

# Route for extensive searching.
@app.route("/browse", methods=['GET', 'POST'])
def browse():
    if request.method == 'POST':

        # Get values from form.
        brand = request.form.get('brand')
        minSize = request.form.get('minSize')
        maxSize = request.form.get('maxSize')
        OS = request.form.get('OS')
        camera = request.form.get('camera')
        SIM = request.form.get('SIM')
        multitouch = request.form.get('multitouch')
        NFC = request.form.get('NFC')
        year = request.form.get('year')

        # If no brand was put in.
        if not brand:

            # Get the 100 latest phones.
            phones = fon.getlatest(100)

            # Filter phones according to user input.
            phones = phone_filter(phones, minSize, maxSize, OS, camera, SIM, multitouch, NFC, year)

            # If phones is empty, no result.
            if not phones:
                flash('Geen resultaten gevonden op basis van deze zoekopdracht', 'alert-warning')
            return render_template("browse.html", phones=phones)

        # If brand was put in
        else:

            # Get the 100 latest phones of a certain brand.
            phones = fon.getlatestBrand(100, brand)

            # Filter phones according to user input.
            phones = phone_filter(phones, minSize, maxSize, OS, camera, SIM, multitouch, NFC, year)

            # If phones is empty, no result.
            if not phones:
                flash('Geen resultaten gevonden op basis van deze zoekopdracht', 'alert-warning')
            return render_template("browse.html", phones=phones)

	# By default, show latest 100 phones.
    else:
        phones = fon.getlatest(100)
        return render_template("browse.html", phones=phones)

# Route for deleting a specific post.
@app.route("/delete", methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':

		# Get the post ID
        post_id = request.form.get('post_id')

        # Remove the post from the database.
        delete = Post.query.filter_by(id=post_id).delete()

        # Remove the replies on particular post
        delete_replies = Reply.query.filter_by(post_id=post_id).delete()
        db.session.commit()

		# Return to the persons profile.
        return redirect("profiel/" + current_user.username)
