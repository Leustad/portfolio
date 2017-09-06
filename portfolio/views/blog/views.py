from flask import render_template, Blueprint, request, flash, redirect, url_for
from portfolio.views.blog.forms import AddPostForm
from portfolio import flatpages
from portfolio import app

blog_blueprint = Blueprint('blog', __name__)

POST_DIR = app.config['POST_DIR']


@blog_blueprint.route('/blogs', methods=['GET'])
def main():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=False)
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
        return redirect(url_for('add_post'))

    return render_template('add_post.html', form=form, error=error)
