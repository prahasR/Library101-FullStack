from datetime import datetime
from web_App import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    if User.query.get(int(user_id)):
        #login_manager.login_view='login'
        return User.query.get(int(user_id))
    elif Librarian.query.get(int(user_id)):
        #login_manager.login_view='lib_login'
        return Librarian.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    token=db.Column(db.String(20),nullable=True)
    
    
    books = db.relationship('Irequest', backref='issuer', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}','{self.token}')"

class Irequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    confirmation_status = db.Column(db.String(20), nullable=False, default='wait')

    book_entry_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_name = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    #e_mail = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Irequest('{self.user_name}', '{self.book_name}', '{self.book_entry_id}','{self.duration}')"


class Librarian(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    token=db.Column(db.String(20),unique=True,nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Librarian('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    #date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    rating= db.Column(db.Integer, nullable=False, default=0)
    username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.description}', '{self.username}','{self.book_id}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(40))
    writer = db.Column(db.String(20), nullable=False)
    publisher=db.Column(db.String(20), nullable=False)#db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    summary = db.Column(db.String(200), nullable=False)#db.Column(db.Text, nullable=False)
    availability=db.Column(db.Integer, nullable=False, default=0)
    img_file = db.Column(db.String(20), nullable=False, default='default1.jpeg')
    rating = db.Column(db.Integer ,nullable=False, default=0)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('Post', backref='owner', lazy=True)
    issued = db.relationship('Irequest', backref='issued', lazy=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.genre}','{self.writer}', '{self.img_file}','{self.publisher}', '{self.availability}')"

