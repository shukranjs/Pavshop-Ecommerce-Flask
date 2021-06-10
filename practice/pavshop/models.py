from pavshop import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Blog(db.Model):

    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.now)
    short_description = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), default='uploads/default.jpeg')
    category_id = db.Column(db.Integer, db.ForeignKey('blogcategory.id'), nullable=False)

    def __repr__(self):
        return f'Blog {self.title}'

class BlogCategory(db.Model):

    __tablename__ = 'blogcategory'
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(100), nullable=False)
    category = db.relationship(Blog, backref='blogcategories', lazy=True, cascade='all,delete')

    def __repr__(self):
        return f'Category {self.blog_title}'


class User(db.Model, UserMixin):

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    parol = db.Column(db.String(100))
    image = db.Column(db.String(20), default='static/uploads/default.jpeg')
    bio = db.Column(db.Text)
    posts = db.relationship('UserPost', backref='post_author', lazy=True, cascade='all, delete')
    def __repr__(self):
        return self.full_name


class UserPost(db.Model, UserMixin):

    __tablename__ = 'userpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    short_description = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.title
