from flask import render_template, Blueprint
blog_blueprint = Blueprint('blog', __name__)


@blog_blueprint.route('/blog', methods=['GET'])
def main():
    return render_template('blog.html')

