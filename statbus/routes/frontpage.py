from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint("frontpage", __name__)


@bp.route("/")
def index():
    return redirect(url_for('rounds.index'))