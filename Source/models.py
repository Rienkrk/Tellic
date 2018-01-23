from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    posts = db.relationship('Post', backref='user', lazy=True)
    replies = db.relationship('Reply', backref='userR', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    replies = db.relationship('Reply', backref='user', lazy=True)

    def __init__(self, user_id, title, text):
        self.user_id = user_id
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Title %r>' % self.title

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(80), nullable=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, user_id, post_id, text, phone):
        self.user_id = user_id
        self.post_id = post_id
        self.text = text
        self.phone = phone

    def __repr__(self):
        return '<Title %r>' % self.title

db.create_all()
