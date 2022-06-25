import math
from datetime import date, datetime, timedelta

from flask import Blueprint, render_template, request, abort, session, g
from sqlalchemy import func

from statbus.ext import cache, db
from statbus.models import (
    Ban,
    Round,
    Death,
    Connection,
    Feedback,
    Player,
    PollOption,
    PollQuestion,
    PollTextReply,
    PollQuestion,
)

from statbus.utils import github


bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/session")
@cache.cached()
def userinfo():
    print(session)
    if "auth.token" in session and "userinfo" not in session:
        private_token = session["auth.token"]
        session["userinfo"] = g.tg_auth.get_user_data(private_token)
    if "userinfo" not in session:
        abort(401)
    return session["userinfo"]


@bp.route("/summary")
@cache.cached()
def summary():
    rounds = (
        Round.query.filter(Round.end_datetime != None)
        .order_by(Round.id.desc())
        .limit(10)
        .all()
    )
    polls = (
        PollQuestion.query.filter(PollQuestion.endtime > datetime.now())
        .order_by(PollQuestion.id.desc())
        .limit(3)
        .all()
    )

    total_rounds = Round.query.count()
    total_players = Player.query.count()

    return {
        "stats": {"rounds": total_rounds, "players": total_players},
        "rounds": [r.id for r in rounds],
        "polls": [p.id for p in polls],
    }


@bp.route("/winrate")
@cache.cached(query_string=True)
def winrate():
    delta = min(90, request.args.get("delta", 7, int))
    showall = request.args.get("showall", False, bool)
    winrates = (
        db.session.query(
            Round.game_mode_result, Round.game_mode, func.count(Round.game_mode_result)
        )
        .filter(Round.end_datetime > datetime.now() - timedelta(days=delta))
        .filter(Round.map_name != "Whiskey Outpost")
        .group_by(Round.game_mode_result, Round.game_mode)
        .all()
    )

    valid_winrates = [
        "Marine Major Victory",
        "Marine Minor Victory",
        "Xenomorph Major Victory",
        "Xenomorph Minor Victory",
    ]

    summary, raw = {}, {}
    for result, game_mode, wins in winrates:
        if result is None or result not in valid_winrates and not showall:
            continue
        if game_mode not in raw:
            raw[game_mode] = {}

        if result not in summary:
            summary[result] = 0
        raw[game_mode][result] = wins
        summary[result] += wins
    return {
        "winrates": summary,
        "by_gamemode": raw,
    }


##
# Get Rounds by page
#
# Returns a paginated result of rounds
##
@bp.route("/rounds")
@bp.route("/rounds/<int:page>")
@cache.cached()
def rounds(page=1):
    page = page - 1
    per_page_limit = min(
        30, int(request.args.get("limit", 10))
    )  # Cap at 30, so we don't hammer a db

    rounds = (
        Round.query.filter(Round.end_datetime != None)
        .order_by(Round.id.desc())
        .limit(per_page_limit)
        .offset(per_page_limit * page)
        .all()
    )

    total_rounds = math.ceil(Round.query.count() / per_page_limit)
    return {
        "rounds": [r.id for r in rounds],
        "page": {"total": total_rounds, "current": page, "per_page": per_page_limit},
    }


##
# Get Specific Round
#
# Returns a specific round by ID
##
@bp.route("/round/<int:round_id>")
@cache.memoize()
def round(round_id):
    round_info = Round.query.filter(Round.id == round_id).first()
    if not round_info or not round_info.end_datetime:
        # We return 404 on rounds that haven't ended to ensure we don't give up too much information
        abort(404)

    connections = 0
    players = []
    try:
        connections = round_info.connections.count()
        players = [
            player.to_object()
            for player in round_info.connections.group_by(Connection.ckey).all()
        ]
    except:
        pass

    deaths = []
    try:
        deaths = [
            death.to_object()
            for death in round_info.deaths.filter(Death.z_coord != 1).all()
        ]
    except:
        pass

    data = {
        **round_info.to_object(),
        "connections": connections,
        "players": players,
        "deaths": deaths,
    }

    return {"round": data}


##
# Get Specific Round
#
# Returns a specific round by ID
##
@bp.route("/polls")
@bp.route("/polls/<int:page>")
@cache.cached()
def polls(page=1):
    page = page - 1
    per_page_limit = min(
        100, int(request.args.get("limit", 30))
    )  # Cap at 100, so we don't hammer a db

    polls = (
        PollQuestion.query.order_by(PollQuestion.id.desc())
        .limit(per_page_limit)
        .offset(per_page_limit * page)
        .all()
    )

    total_polls = math.ceil(PollQuestion.query.count() / per_page_limit)
    return {
        "polls": {r.id: r.to_object() for r in polls},
        "error": None,
        "page": {"total": total_polls, "current": page, "per_page": per_page_limit},
    }


@bp.route("/poll/<int:poll_id>")
@cache.memoize()
def poll(poll_id):
    poll_info = PollQuestion.query.filter(PollQuestion.id == poll_id).first()
    if not poll_info:
        # We return 404 on rounds that haven't ended to ensure we don't give up too much information
        abort(404)

    return {"poll": poll_info.to_object(), "error": None}


##
# Get Specific Round
#
# Returns a specific round by ID
##
@bp.route("/bans")
@bp.route("/bans/<int:page>")
@cache.memoize()
def bans(page=1):
    page = page - 1
    per_page_limit = min(
        100, int(request.args.get("limit", 30))
    )  # Cap at 100, so we don't hammer a db

    admin = request.args.get("admin", "")[:64]
    ckey = request.args.get("ckey", "")[:64]
    server_only = bool(request.args.get("server_only", False))
    perma = bool(request.args.get("perma", False))

    bans = Ban.query

    if admin:
        bans = bans.filter(Ban.a_ckey == admin)
    if ckey:
        bans = bans.filter(Ban.ckey == ckey)
    if server_only:
        bans = bans.filter(Ban.role == "Server")
    if perma:
        bans = bans.filter(Ban.expiration_time == None, Ban.unbanned_datetime == None)

    ban_list = (
        bans.order_by(Ban.id.desc())
        .limit(per_page_limit)
        .offset(per_page_limit * page)
        .all()
    )

    total_bans = math.ceil(bans.count() / per_page_limit)
    return {
        "bans": {r.id: r.to_object() for r in ban_list},
        "error": None,
        "page": {
            "total": total_bans,
            "current": (page + 1),
            "per_page": per_page_limit,
        },
    }

