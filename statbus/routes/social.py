from flask import Blueprint, render_template, request, redirect, url_for, current_app
from statbus.models.round import Round
from statbus.models.poll import PollQuestion

bp = Blueprint("social", __name__)


@bp.route("/play-now")
def play():
    return redirect(current_app.config["SOCIAL_LINK_PLAYNOW"])


@bp.route("/discord")
def discord():
    return redirect(current_app.config["SOCIAL_LINK_DISCORD"])


@bp.route("/github")
def github():
    return redirect(current_app.config["SOCIAL_LINK_GITHUB"])


@bp.route("/getting-started")
def getting_started():
    return redirect(current_app.config["SOCIAL_LINK_GETTING_STARTED"])
