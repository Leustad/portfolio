import os
import traceback

from flask import render_template, Blueprint, request, redirect, url_for
from portfolio.views.blog.forms import AddPostForm
from portfolio import flatpages
from portfolio import app

blog_blueprint = Blueprint('blog', __name__)

POST_DIR = app.config['POST_DIR']


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

    return render_template('add_post.html', form=form, error=error)
