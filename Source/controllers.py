from app import *
from models import *
from api import *
<<<<<<< HEAD
import json

# Usually the searchs occurs in databases, for this simple example we're using search in this array
BRAZIL_STATES = [u"Acre - Rio Branco",
u"Alagoas - Maceió",
u"Amapá - Macapá",
u"Amazonas - Manaus",
u"Bahia - Salvador",
u"Ceara - Fortaleza",
u"Distrito Federal - Brasília",
u"Espírito Santo - Vitória",
u"Goiás - Goiânia",
u"Maranhão - São Luiz",
u"Mato Grosso - Cuiabá",
u"Mato Grosso do Sul - Campo Grande",
u"Minas Gerais - Belo Horizonte",
u"Pará - Belém",
u"Paraíba - João Pessoa",
u"Paraná - Curitiba",
u"Pernambuco - Recife",
u"Piauí - Terezina",
u"Rio de Janeiro - Rio de Janeiro",
u"Rio Grande do Norte - Natal",
u"Rio Grande do Sul - Porto Alegre",
u"Rondônia - Porto Velho",
u"Roraima - Boa Vista",
u"Santa Catarina - Florianópolis",
u"São Paulo - São Paulo",
u"Sergipe - Aracajú",
u"Tocantins - Palmas"]

@app.route("/search")
def search():
	text = request.args['searchText'] # get the text to search for
	# create an array with the elements of BRAZIL_STATES that contains the string
	# the case is ignored
	result = [c for c in BRAZIL_STATES if unicode(text).lower() in c.lower()]
	# return as JSON
	return json.dumps({"results":result})
=======
from sqlalchemy import desc
>>>>>>> 5404902eb369d7ecd631a2055f69250bcc2e377b

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
            return render_template('register.html')

        elif User.query.filter_by(username=username).first():
            flash("Helaas! Uw gebruikersnaam is al in gebruik!", 'alert-warning')
            return redirect(url_for("register"))

        else:
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
            return redirect(url_for("login"))

        userInstance = User.query.filter_by(username=username).first()

        if not userInstance:
            flash('Oops! U heeft een verkeerd wachtwoord of gebruikersnaam opgegeven!', 'alert-danger')
            return redirect(url_for("login"))
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

        # Add post to database.
        newPost = Post(current_user.id, title, post)
        db.session.add(newPost)
        db.session.commit()

        flash('U heeft uw post succesvol aangemaakt!', 'alert-success')
        return redirect(url_for("index"))

@app.route("/")
def index():

    # get posts from database, most recent first
    posts = Post.query.order_by(desc(Post.created_on)).all()
    return render_template("index.html", posts=posts)

@app.route("/profiel")
@login_required
def profiel():

    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template("profiel.html", posts=posts)

@app.route("/display/<phone>")
def display(phone):
    # Uses the token to get into the API.
    fon = FonApi('3618ac67ea1695322d52be3bca323ac4eb29caca9570dbe5')
    # Get all the information about a specific phone and return the html file.
    phone = fon.getdevice(phone)
    return render_template("display.html", phone=phone)

@app.route("/reply", methods=['GET', 'POST'])
def reply():
    # Get written reply via POST.
    reply = request.form.get("reply")
    post_id = request.form.get("post_id")

    # Add post to database.
    newReply = Reply(current_user.id, post_id, reply, "tjest")
    db.session.add(newReply)
    db.session.commit()

    flash('U heeft uw reply succesvol aangemaakt!', 'alert-success')
    return redirect("post/" + post_id)

@app.route("/post/<post_id>")
def post(post_id):
    if request.method == "GET":
        post = Post.query.filter_by(id=post_id).first()
        replies = Reply.query.filter_by(post_id=post_id).all()
        return render_template("post.html", post=post, replies=replies)

