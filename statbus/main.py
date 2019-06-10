from flask import Flask

from .models import db_wrapper
from .routes import polls


def create_app(**kwargs):
    app = Flask(__name__)

    # Configuration	
    app.config.from_pyfile('./config/config.py')

    
    # Setup database (peewee playhouse)
    db_wrapper.init_app(app)

    # Register blueprints / routes
    app.register_blueprint(polls.bp)

    return app