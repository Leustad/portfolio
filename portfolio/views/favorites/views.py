from flask import render_template, Blueprint
favorites_blueprint = Blueprint('favorites', __name__)


@favorites_blueprint.route('/favorites', methods=['GET'])
def main():
    return render_template('favorites.html')

