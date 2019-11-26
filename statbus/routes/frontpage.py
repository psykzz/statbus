from flask import Blueprint, render_template, request, redirect, url_for
from statbus.database import Round

bp = Blueprint("frontpage", __name__)


@bp.route("/")
def index():
    recent_rounds = Round.get_recent()
    return render_template("index.html", recent_rounds=recent_rounds)
