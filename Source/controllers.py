from app import *
from models import *
from api import *
import requests
import json
from sqlalchemy import desc
from collections import Counter
from helpers import *

# Initialize API.
fon = FonApi('3618ac67ea1695322d52be3bca323ac4eb29caca9570dbe5')

@app.route("/search", methods=['GET', 'POST'])
def search():
	var = request.args['searchText']
	phones = fon.getdevice(var)

	return json.dumps({'phones':phones});

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username=request.form.get("username").lower()
        password=request.form.get("password")
        passwordCheck=request.form.get("passwordCheck")

        if not password or not username or not passwordCheck:
            flash('Oops! Vul alstublieft uw gebruikersnaam en wachtwoord in!', 'alert-danger')
            return redirect(url_for("register"))

        elif password != passwordCheck:
            flash('Oops! Wachtwoorden komen niet overheen!', 'alert-danger')
            return render_template("register.html", username=username, password=password, passwordCheck=passwordCheck)

        elif User.query.filter_by(username=username).first():
            flash("Helaas! Uw gebruikersnaam is al in gebruik!", 'alert-warning')
            return render_template("register.html", username=username, password=password, passwordCheck=passwordCheck)

        # Make sure the username consists of only numbers and letters.
        elif username.isalnum() == False:
            flash("Uw gebruikersnaam mag alleen bestaan uit letters en cijfers!", 'alert-warning')
            return render_template("register.html", username=username, password=password, passwordCheck=passwordCheck)

        # Make sure both username and password have a minimal and maximal length.
        elif len(username) < 5 or len(username) > 15:
            flash("Uw gebruikersnaam dient tussen de 5 en 15 tekens lang zijn!", 'alert-warning')
            return render_template("register.html", username=username, password=password, passwordCheck=passwordCheck)

        elif len(password) < 5 or len(password) > 40:
            flash("Uw wachtwoord dient minimaal 5 tekens lang te zijn!", 'alert-warning')
            return render_template("register.html", username=username, password=password, passwordCheck=passwordCheck)

        else:
            # Add user to database.
            hashedPassword = bcrypt.generate_password_hash(password).decode("utf-8")
            newuser = User(username, hashedPassword)
            db.session.add(newuser)
            db.session.commit()

            login_user(newuser)

            flash("U bent succesvol geregistreerd " + username + "!", 'alert-success')
            return redirect(url_for("index"))

@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username = username).first()

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Om dit te mogen zien moet u ingelogd zijn!', 'alert-warning')
    return redirect("login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username=request.form.get("username").lower()
        password=request.form.get("password")

        if not password or not username:
            flash('Oops! Geef zowel een gebruikersnaam als een wachtwoord op!', 'alert-danger')
            return render_template("login.html", username=username, password=password)

        userInstance = User.query.filter_by(username=username).first()

        if not userInstance:
            flash('Oops! U heeft een verkeerd wachtwoord of gebruikersnaam opgegeven!', 'alert-danger')
            return render_template("login.html", username=username, password=password)
        else:
            if bcrypt.check_password_hash(userInstance.password, password) == True:
                login_user(userInstance)
                flash("U bent succesvol ingelogd " + username + "!", 'alert-success')
                return redirect(url_for("index"))
            else:
                flash('Oops! U heeft een verkeerd wachtwoord of gebruikersnaam opgegeven!', 'alert-danger')
                return redirect(url_for("login"))

@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash('U bent succesvol uitgelogd, tot ziens!', 'alert-success')
    return redirect(url_for("index"))

@app.route("/createPost", methods=['GET', 'POST'])
@login_required
def createPost():

    if request.method == "GET":
        return render_template("createPost.html")

    else:
        # Get written post via POST.
        title = request.form.get("title")
        post = request.form.get("post")

        # Make sure the post has a title and has content.
        if not title:
            flash("Uw post moet een titel hebben!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)

        if len(post) == 0:
            flash("Uw post moet inhoud hebben!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)

        # Make sure the title and post have a cap.
        if len(post) > 1500:
            flash("Uw post mag maximaal uit 1500 tekens bestaan!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)

        elif len(title) > 100:
            flash("Uw titel mag maximaal uit 100 tekens bestaan!", 'alert-warning')
            return render_template("createPost.html", title=title, post=post)

        else:
            # Add post to database.
            newPost = Post(current_user.id, title, post)
            db.session.add(newPost)
            db.session.commit()

            flash('U heeft uw post succesvol aangemaakt!', 'alert-success')
            return redirect(url_for("index"))

@app.route("/")
def index():

    # Get posts from database, most recent first.
    posts = Post.query.order_by(desc(Post.created_on)).all()

    # Get the 3 most popular phones.
    phones = Favorite.query.all()
    popular = Counter([phone.phone for phone in phones]).most_common(3)


    return render_template("index.html", posts=posts, popular=popular)

@app.route("/profiel/<username>")
@login_required
def profiel(username):

    userInstance = User.query.with_entities(User.id).filter_by(username=username).first()
    replies = Reply.query.filter_by(user_id=userInstance[0]).all()
    posts = Post.query.filter_by(user_id=userInstance[0]).all()
    favorites = Favorite.query.filter_by(user_id=userInstance[0]).all()
    return render_template("profiel.html", posts=posts, replies=replies, favorites=favorites)

@app.route("/display/<phone>")
def display(phone):

    # Get image from Qwant API
    image = Qwant.get_image(phone)
    # Get specifications from fonAPI
    phone = fon.getdevice(phone)
    return render_template("display.html", phone=phone, image=image)


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
	else:

	    # Add post to database.
	    newReply = Reply(current_user.id, post_id, reply, phone)
	    db.session.add(newReply)
	    db.session.commit()

	    flash('U heeft uw reply succesvol aangemaakt!', 'alert-success')
	    return redirect("post/" + post_id)

@app.route("/post/<post_id>")
def post(post_id):
    if request.method == "GET":

        # Get clicked post.
        post = Post.query.filter_by(id=post_id).first()

        # Get replies of post.
        replies = Reply.query.filter_by(post_id=post_id).order_by(desc(Reply.created_on)).all()

        return render_template("post.html", post=post, replies=replies)

@app.route("/favorite", methods=['GET', 'POST'])
def favorite():

    # Get phone name from hidden form.
    phone = request.form.get('phone')
    if not Favorite.query.filter_by(user_id=current_user.id, phone=phone).first():

        # Add favorite to database.
        addFavorite = Favorite(current_user.id, phone)
        db.session.add(addFavorite)
        db.session.commit()

        flash('Deze telefoon is toegevoegd aan uw favorieten!', 'alert-success')

    else:
        flash('Deze telefoon staat al in uw favorieten', 'alert-warning')

    return redirect("display/" + phone)


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

    else:

        # By default, show latest 100 phones.
        phones = fon.getlatest(100)
        return render_template("browse.html", phones=phones)

@app.route("/delete", methods=['GET', 'POST'])
def delete():

    post = request.form.get('post')
    text = request.form.get('text')

    # Remove the post from the database.
    delPost = Post(current_user.id, post, text)
    db.session.delete(delPost)
    db.session.commit()

