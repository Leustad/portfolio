import os
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print('__APP_SETTINGS__: {}'.format(os.environ['APP_SETTINGS']))
# app.secret_key = os.urandom(24)
# app.config.from_pyfile('_config.py')
# bcrypt = Bcrypt(app)
# db = SQLAlchemy(app)

from portfolio.views.main.views import main_blueprint
from portfolio.views.portfolio.views import portfolio_blueprint
from portfolio.views.projects.views import projects_blueprint
from portfolio.views.blog.views import blog_blueprint
from portfolio.views.favorites.views import favorites_blueprint

# Register the blueprints
app.register_blueprint(main_blueprint)
app.register_blueprint(portfolio_blueprint)
app.register_blueprint(projects_blueprint)
app.register_blueprint(blog_blueprint)
app.register_blueprint(favorites_blueprint)
