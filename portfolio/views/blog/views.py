from flask import flash, redirect, render_template, request, session, url_for, Blueprint
blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/blog', methods=['GET'])
def main():
    return render_template('blog.html')

