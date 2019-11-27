from flask import Blueprint, render_template, request, redirect, url_for

from statbus.database import Round, PollQuestion
from statbus.ext import cache

bp = Blueprint("frontpage", __name__)


@bp.route("/")
@cache.cached()
def index():
    active_polls = PollQuestion.get_active()
    recent_rounds = Round.get_recent()
    return render_template(
        "index.html", recent_rounds=recent_rounds, active_polls=active_polls
    )
