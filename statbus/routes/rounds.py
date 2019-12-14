from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, abort
from playhouse.flask_utils import PaginatedQuery

from statbus.models.player import Player
from statbus.models.round import Round
from statbus.ext import cache
from statbus.utils import github


bp = Blueprint("rounds", __name__)


@bp.route("/round")
@bp.route("/rounds")
@cache.cached()
def index():
    rounds = Round.select().order_by(Round.id.desc())
    pages = PaginatedQuery(rounds, 10)
    return render_template("rounds/rounds.html", pages=pages)


@bp.route("/rounds/<int:round_id>")
@cache.memoize()
def detail(round_id):
    round_info = Round.select().where(Round.id == round_id).first()
    if not round_info:
        abort(404)

    pr_list = round_info.merged_prs
    balance_prs = github.get_balance_prs()

    return render_template(
        "rounds/round_info.html", round_info=round_info, balance_prs=balance_prs
    )


@bp.route("/rounds/<string:player_name>")
@cache.memoize()
def by_player(player_name):
    player = Player.select().where(Player.ckey == player_name).first()
    if not player:
        abort(404)

    pages = PaginatedQuery(player.rounds, 10)
    return render_template("rounds/rounds.html", pages=pages, for_player=player_name)


@bp.route("/rounds/winrates")
@cache.cached()
def recent_winrates():
    rounds = (
        Round.select(Round.game_mode, Round.game_mode_result, Round.map_name)
        .order_by(Round.id.desc())
        .where(Round.initialize_datetime > (datetime.now() - timedelta(days=30)))
    )

    winrates = None

    return render_template("rounds/winrates.html", winrates=winrates, rounds=rounds)
