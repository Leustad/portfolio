import os
import traceback
from functools import wraps

from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from portfolio.views.blog.forms import AddPostForm, LoginForm
from portfolio import flatpages, app, bcrypt

blog_blueprint = Blueprint('blog', __name__)
POST_DIR = app.config['POST_DIR']

usrname = app.config['USRNAME']
smth = app.config['SMTH']


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in !!')
            return redirect(url_for('blog.login'))

    return wrap


def save_post(title, body):
    basedir = os.path.abspath(os.path.dirname(__file__))
    file_name = str(title).rstrip('\n') + '.md'
    write_path = os.path.join(basedir, 'content', 'posts', file_name)
    print('write path: ' + write_path)
    body1 = body.splitlines()
    with open(write_path, 'w') as f:
        f.write('title: ' + title + '\n')
        f.write('\r'.join(body1))


@blog_blueprint.route('/blogs', methods=['GET'])
def main():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=True)
    return render_template('blogs.html', posts=posts)


@app.route('/blog/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('blog.html', post=post)


@blog_blueprint.route('/admin/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    error = None
    form = AddPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        print('Received new post data')
        blog_title = form.blog_title.data
        blog_body = form.blog_body.data
        print('blog body:' + blog_body)
        try:
            save_post(blog_title, blog_body)
        except Exception as e:
            traceback.print_exc()
        return redirect(url_for('blog.add_post'))

    return render_template('add_post.html', form=form, error=error, next=request.path)


@blog_blueprint.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    error = None

    if request.method == 'POST' and form.validate_on_submit():
        if bcrypt.check_password_hash(smth, request.form['password']) and \
                bcrypt.check_password_hash(usrname, request.form['username']):
            session['logged_in'] = True
            error = None
            return redirect(url_for('blog.add_post'))
        else:
            error = 'Wrong Username or Password!'
    return render_template('login.html', form=form, error=error)


@blog_blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main.main'))


def find_the_post(name):
    path = '{}/{}'.format(POST_DIR, name)
    return flatpages.get_or_404(path)


def delete_post(title):
    basedir = os.path.abspath(os.path.dirname(__file__))
    path_to_remove = os.path.join(basedir, 'content', 'posts', title + '.md')
    os.remove(path_to_remove)


@blog_blueprint.route('/edit/<title>', methods=['GET', 'POST'])
@login_required
def edit(title):
    path = '{}/{}'.format(POST_DIR, title)
    post = flatpages.get_or_404(path)

    title = post['title'].rstrip()
    date = post['date']
    body = 'date: ' + str(date) + '\n\n' + post.body

    form = AddPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        save_post(form.blog_title.data, form.blog_body.data)
        return redirect('/blog/{}'.format(post['title']))

    form.blog_title.data = title
    form.blog_body.data = body
    return render_template('edit_post.html', form=form)


@blog_blueprint.route('/delete/<title>')
@login_required
def delete(title):
    error = None
    try:
        delete_post(title)
    except FileNotFoundError as e:
        print(e)
    return redirect(url_for('blog.main'))
