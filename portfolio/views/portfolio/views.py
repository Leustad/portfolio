from flask import Blueprint, render_template

portfolio_blueprint = Blueprint('portfolio', __name__)


@portfolio_blueprint.route('/portfolio', methods=['GET'])
def portfolio():
    return  render_template('portfolio.html')
