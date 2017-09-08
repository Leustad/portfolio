from flask import render_template, Blueprint

projects_blueprint = Blueprint('projects', __name__)


@projects_blueprint.route('/projects', methods=['GET'])
def main():
    return render_template('projects.html')
