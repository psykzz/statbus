from flask import Flask, render_template

from statbus.ext import cache, cors, db, session
from statbus.routes import api, auth


def create_app(test_config=None):
    app = Flask(__name__)

    # Configuration
    app.config.from_pyfile("./config/config.py")

    if test_config:
        app.config.update(test_config)

    # Setup extentions
    session.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    cors.init_app(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # Blueprints
    app.register_blueprint(api.bp)
    # app.register_blueprint(frontpage.bp)
    # app.register_blueprint(personal.bp)
    # app.register_blueprint(social.bp)
    app.register_blueprint(auth.bp)
    # app.register_blueprint(polls.bp)
    # app.register_blueprint(rounds.bp)

    # Generic handler
    # @app.errorhandler(500)
    # def internal_error(exc):
    #     return render_template("error.html", error=exc), 500

    return app
