from flask import flash, redirect, render_template, request, session, url_for, Blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET'])
def main():
    return render_template('index.html')

