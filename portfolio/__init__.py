import os

from flask import Flask
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer
from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
flatpages = FlatPages(app)
freezer = Freezer(app)
print('__APP_SETTINGS__: {}'.format(os.environ['APP_SETTINGS']))

bcrypt = Bcrypt(app)
# db = SQLAlchemy(app)

from portfolio.views.main.views import main_blueprint
from portfolio.views.portfolio.views import portfolio_blueprint
from portfolio.views.projects.views import projects_blueprint
from portfolio.views.blog.views import blog_blueprint
from portfolio.views.favorites.views import favorites_blueprint
from portfolio.views.error import main  # ==> Error Handling

# Register the blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(portfolio_blueprint)
app.register_blueprint(projects_blueprint)
app.register_blueprint(blog_blueprint)
app.register_blueprint(favorites_blueprint)


@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type':"text/css"}