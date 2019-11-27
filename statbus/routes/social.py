from flask import Blueprint, render_template, request, redirect, url_for, current_app
from statbus.database import Round, PollQuestion

bp = Blueprint("social", __name__)


@bp.route("/discord")
def discord():
    return redirect(current_app.config['SOCIAL_LINK_DISCORD'])

@bp.route("/github")
def github():
    return redirect(current_app.config['SOCIAL_LINK_GITHUB'])

@bp.route("/getting-started")
def getting_started():
    return redirect(current_app.config['SOCIAL_LINK_GETTING_STARTED'])