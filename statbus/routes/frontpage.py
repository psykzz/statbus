from flask import Blueprint, render_template, request

bp = Blueprint("frontpage", __name__)


@bp.route("/")
def index():
    return render_template("index.html")
