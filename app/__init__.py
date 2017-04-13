from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import time

db = SQLAlchemy()
mail = Mail()
moment = Moment()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'

from app import models

User = models.User
Blog = models.Blog
Comment = models.Comment
Tag = models.Tag
TagBlog = models.TagBlog

def datetime_filter(t):
    delta = int(time.time()-float(t))
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    env = app.jinja_env
    env.filters['datetime'] = datetime_filter

    config[config_name].init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
