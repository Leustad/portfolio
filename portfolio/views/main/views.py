from flask import render_template, Blueprint

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET'])
def main():
    return render_template('index.html')
