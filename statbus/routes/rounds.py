from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, abort
from playhouse.flask_utils import PaginatedQuery

from statbus.database import Round
from statbus.cache import cache


bp = Blueprint("rounds", __name__)


@bp.route("/round")
@bp.route("/rounds")
@cache.cached(timeout=60)
def index():
    rounds = Round.select().order_by(Round.id.desc())
    pages = PaginatedQuery(rounds, 10)
    return render_template("rounds/rounds.html", pages=pages)


@bp.route("/rounds/<int:round_id>")
@cache.cached(timeout=60)
def detail(round_id):
    round_info = Round.select().where(Round.id == round_id).first()
    if not round_info:
        abort(404)
    return render_template("rounds/round_info.html", round_info=round_info)


@bp.route("/rounds/winrates")
@cache.cached(timeout=60)
def recent_winrates():
    rounds = (
        Round.select(Round.game_mode, Round.game_mode_result, Round.map_name)
        .order_by(Round.id.desc())
        .where(Round.initialize_datetime > (datetime.now() - timedelta(days=30)))
    )

    winrates = None

    return render_template("rounds/winrates.html", winrates=winrates, rounds=rounds)
