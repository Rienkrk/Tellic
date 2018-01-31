from app import db

class User(db.Model):

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    posts = db.relationship('Post', backref='user', lazy=True)
    replies = db.relationship('Reply', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    # Is True when user is logged in.
    def is_active(self):
        return True

    # Combine username to get_id function.
    def get_id(self):
        return self.username

    # [Not Relevant] If user is authenticated (normally when mail is confirmed). Always true.
    def is_authenticated(self):
        return True

    # [Not Relevant] If user is anonymous, is always false.
    def is_anonymous(self):
        return False

class Post(db.Model):

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    replies = db.relationship('Reply', backref='post', lazy=True)

    def __init__(self, user_id, title, text):
        self.user_id = user_id
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Title %r>' % self.title

class Reply(db.Model):

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    # Relationships
    posts = db.relationship('Post', backref='reply', lazy=True)

    def __init__(self, user_id, post_id, text, phone):
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.phone = phone

    def __repr__(self):
        return '<Title %r>' % self.title

class Favorite(db.Model):

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone = db.Column(db.String(80), nullable=False)

    def __init__(self, user_id, phone):
        self.user_id = user_id
        self.phone = phone

# Create database when none exist.
db.create_all()
