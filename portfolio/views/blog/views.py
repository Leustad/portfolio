import os
import traceback
from functools import wraps

from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from portfolio.views.blog.forms import AddPostForm, LoginForm
from portfolio import flatpages, app, bcrypt

SMTH = b'$2b$12$D9fukiXJ5Ik7LE1FpjgIB.xhZg1ln2pTCd/J3IVXAbun3dWSNxml6'

blog_blueprint = Blueprint('blog', __name__)

POST_DIR = app.config['POST_DIR']


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
    file_name = str(title) + '.md'
    write_path = os.path.join(basedir, 'content', 'posts', file_name)
    print('write path: ' + write_path)

    with open(write_path, 'w') as f:
        f.write('title: ' + title + '\n')
        f.write(body)


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

    if request.method == 'POST' and form.validate_on_submit():
        if bcrypt.check_password_hash(SMTH, request.form['password']) and request.form['username'] == 'Leustad':
            session['logged_in'] = True
            return redirect(url_for('blog.add_post'))
        else:
            flash('Wrong Password!')
            print('Wrong Password')
    return render_template('login.html', form=form)


@blog_blueprint.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main.main'))
