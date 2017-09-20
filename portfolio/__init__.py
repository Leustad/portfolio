import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_assets import Environment, Bundle
from flask_compress import Compress
from flask_caching import Cache

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print('__APP_SETTINGS__: {}'.format(os.environ['APP_SETTINGS']))

bundles = {
    'js_bundle': Bundle('js/main.js', filters='jsmin', output='gen/js_min.js'),
    'css_bundle': Bundle('css/style.css', filters='cssmin', output='gen/style_min.css') 
}

assets = Environment(app)
assets.register(bundles)

bcrypt = Bcrypt(app)
Compress(app)
cache = Cache(config={'CACHE_TYPE': 'simple'})

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
