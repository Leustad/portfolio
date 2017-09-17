import traceback
from functools import wraps

from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from bs4 import BeautifulSoup
import bleach

from portfolio.views.blog.forms import AddPostForm, LoginForm
from portfolio import app, bcrypt
from portfolio.aws_funcs import aws_func

blog_blueprint = Blueprint('blog', __name__)

usrname = app.config['USRNAME']
smth = app.config['SMTH']

VALID_TAGS = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
              'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
              'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
              'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
              'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
              'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
              'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
              'thead', 'tr', 'tt', 'u', 'ul', 'var', 'iframe', 'frameborder', 'allowfullscreen']

VALID_ATTRIBUTES = ['abbr', 'accept', 'accept-charset', 'accesskey',
                    'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
                    'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
                    'colspan', 'color', 'compact', 'coords', 'datetime', 'dir',
                    'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
                    'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
                    'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt',
                    'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
                    'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
                    'usemap', 'valign', 'value', 'vspace', 'width']


def sanitize_html(value):
    soup = BeautifulSoup(bleach.clean(value, tags=VALID_TAGS, attributes=VALID_ATTRIBUTES), "html5lib")
    return soup.renderContents()


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to log in !!')
            return redirect(url_for('blog.login'))

    return wrap


@blog_blueprint.route('/blogs', methods=['GET'])
def main():
    posts = aws_func.get_all_posts()
    return render_template('blogs.html', posts=posts)


@app.route('/blog/<name>/')
def post(name):
    content = []
    post_title, post_body = aws_func.get_single_post(name)
    post_body = post_body.split('\r\n')
    for line in post_body:
        content.append(str(sanitize_html(line)))
    return render_template('blog.html', post_title=post_title, post_body=content)


@blog_blueprint.route('/admin/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    error = None
    form = AddPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        print('Received new post data')
        blog_title = form.blog_title.data
        blog_body = form.blog_body.data
        try:
            aws_func.upload_to_s3(blog_title, blog_body)
        except Exception as e:
            print(e)
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


@blog_blueprint.route('/edit/<title>', methods=['GET', 'POST'])
@login_required
def edit(title):
    # TODO: S3 file manipulation can only be done with deleting and adding the new file.

    # path = '{}/{}'.format(POST_DIR, title)
    # # post = flatpages.get_or_404(path)
    #
    # title = post['title'].rstrip()
    # date = post['date']
    # body = 'date: ' + str(date) + '\n\n' + post.body
    #
    # form = AddPostForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     # save_post(form.blog_title.data, form.blog_body.data)
    #     return redirect('/blog/{}'.format(post['title']))
    #
    # form.blog_title.data = title
    # form.blog_body.data = body
    # return render_template('edit_post.html', form=form)
    return redirect(url_for('main.main'))


@blog_blueprint.route('/delete/<title>')
@login_required
def delete(title):
    try:
        aws_func.delete_from_s3(title)
    except Exception as e:
        print(e)
    return redirect(url_for('blog.main'))
