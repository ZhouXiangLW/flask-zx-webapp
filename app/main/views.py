from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from wtforms import RadioField
from wtforms.validators import Required
from markdown2 import markdown

from . import main
from . import LoginForm, RegisterForm
from app import db, User, Blog, Comment, Tag, TagBlog

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/blogs/<tag>/<page>')
def blogs(tag,page):
    tags = Tag.query.all()
    if tag == 'all':
        blogs = Blog.query.paginate(int(page),5,False)
    else:
        blogs = db.session.query(Blog).join(TagBlog).join(Tag). \
                                filter(Tag.name.like(tag)). \
                                paginate(int(page), 5, False)
    for blog in blogs.items:
        blog.summary = blog.content[:100]
    return render_template('blogs.html', blogs=blogs, tags=tags, caregory=tag)

@main.route('/login', methods=['GET','POST'])
def login():
    email = None
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and form.passwd.data == user.passwd:
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        if user is None:
            flash('用户不存在')
        if user is not None and form.passwd.data != user.passwd:
            flash('密码错误，请重新输入')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        passwd = form.passwd.data
        email = form.email.data
        user = User(name=name, passwd=passwd, email=email)
        try:
            db.session.add(user)
            b.session.commit()
        except:
            flash('无法注册，请重试！')
        if form.remember_me.data:
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        return redirect(url_for('main.index'))
    return render_template('register.html', form=form)

@main.route('/createblog', methods=['GET', 'POST'])
def create_blog():
    tags = Tag.query.all()
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        keywords = request.form['keywords']
        blog = Blog(name=name, content=content, keywords=keywords)
        db.session.add(blog)
        for tag in tags:
            try:
                blogtag = request.form[tag.en_name]
            except:
                pass
            else:
                tag_id = Tag.query.filter_by(en_name=tag.en_name).first().id
                blog_id = blog.id
                tag_blog = TagBlog(blog_id=blog_id, tag_id=tag_id)
                db.session.add(tag_blog)
        db.session.commit()
    return render_template('createblog.html', tags=tags)

@main.route('/blog/<id>')
def get_blog(id):
    blog = Blog.query.filter_by(id=id).first()
    html_content = markdown(blog.content)
    return render_template('blog.html', blog=blog, html_content=html_content)
