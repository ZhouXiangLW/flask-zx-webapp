# coding: utf-8
from sqlalchemy import BigInteger, Column, Float, Integer, String, ForeignKey
import time, uuid
from app import db, login_manager
from flask_login import UserMixin

def next_id():
    return '%015d%s000' % (int(time.time()*1000), uuid.uuid4().hex)
    
class Blog(db.Model):
    __tablename__ = 'blogs'

    id = Column(String(50), primary_key=True)
    title = Column(String(50), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(Float(asdecimal=True), nullable=False)
    rd_times = Column(BigInteger, nullable=False)
    keywords = Column(String(255), nullable=False)

    def __init__(self ,**kw):

        self.id = next_id() or kw['id']
        self.created_at = time.time()
        self.rd_times = 0
        self.content = kw['content']
        self.title = kw['title']
        self.keywords = kw['keywords']



    def __repr__(self):
        return '<Blog %r>' % self.title


class Comment(db.Model):
    __tablename__ = 'comments'

    id = Column(String(50), primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(Float(asdecimal=True), nullable=False)

    def __init__(self ,**kw):

        self.id = next_id() or kw['id']
        self.created_at = time.time()
        self.content = kw['content']

    def __repr__(self):
        return '<Comment %r>' % self.content


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(String(50), primary_key=True)
    email = Column(String(50), nullable=False)
    passwd = Column(String(50), nullable=False)
    admin = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    image = Column(String(500), nullable=False)
    created_at = Column(Float(asdecimal=True), nullable=False)

    def __init__(self ,**kw):

        self.id = next_id() or kw['id']
        self.created_at = time.time()
        self.passwd = kw['passwd']
        self.admin = 0
        self.name = kw['name']
        self.image = '/static/img/user.png'
        self.email = kw['email']

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.name

class BlogComment(db.Model):
    __tablename__ = 'blog_comment'

    id = Column(String(255), primary_key=True)
    blog_id = Column(String(255),ForeignKey('blogs.id'), nullable=False)
    comment_id = Column(String(255),ForeignKey('comments.id'), nullable=False)

    def __init__(self, **kw):
        self.id = next_id()
        self.blog_id = kw['blog_id']
        self.comment_id = kw['comment_id']



class TagBlog(db.Model):
    __tablename__ = 'tag_blog'

    id = Column(String(255), primary_key=True)
    tag_id = Column(String(255),ForeignKey('tags.id'), nullable=False)
    blog_id = Column(String(255),ForeignKey('blogs.id'), nullable=False)

    def __init__(self, **kw):
        self.id = next_id()
        self.blog_id = kw['blog_id']
        self.tag_id = kw['tag_id']


class Tag(db.Model):
    __tablename__ = 'tags'

    id = Column(String(255), primary_key=True)
    name = Column(String(50), nullable=False)
    en_name = Column(String(50), nullable=False)

    def __init__(self, **kw):
        self.id = next_id()
        self.name = kw['name']


class UserBlog(db.Model):
    __tablename__ = 'user_blog'

    id = Column(String(255), primary_key=True)
    user_id = Column(String(255),ForeignKey('users.id'), nullable=False)
    blog_id = Column(String(255), ForeignKey('blogs.id'), nullable=False)

    def __init__(self, **kw):
        self.id = next_id()
        self.blog_id = kw['blog_id']
        self.user_id = kw['user_id']

@login_manager.user_loader
def load_user(id):
    return User.query.get(str(id))
