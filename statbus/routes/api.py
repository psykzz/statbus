import math
from datetime import date, datetime, timedelta

from flask import Blueprint, render_template, request, abort, session, g
from sqlalchemy import func

from statbus.ext import cache, db
from statbus.models import (
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
        db.session.query(Round.game_mode_result, func.count(Round.game_mode_result))
        .filter(Round.end_datetime > datetime.now() - timedelta(days=delta))
        .filter(Round.map_name != "Whiskey Outpost")
        .group_by(Round.game_mode_result)
        .all()
    )

    valid_winrates = [
        "Marine Major Victory",
        "Marine Minor Victory",
        "Xenomorph Major Victory",
        "Xenomorph Minor Victory",
    ]

    return {
        "winrates": {
            k: v
            for k, v in winrates
            if k is not None and k in valid_winrates or showall
        },
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

    players = [
        player.to_object()
        for player in round_info.connections.group_by(Connection.ckey).all()
    ]
    deaths = [
        death.to_object()
        for death in round_info.deaths.filter(Death.z_coord != 1).all()
    ]

    data = {
        **round_info.to_object(),
        "connections": round_info.connections.count(),
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
    poll_info = PollQuestion.query.filter(Poll.id == poll_id).first()
    if not poll_info or not poll_info.enddate:
        # We return 404 on rounds that haven't ended to ensure we don't give up too much information
        abort(404)

    return {"round": poll_info.to_object(), "error": None}


# @bp.route("/rounds/<string:player_name>")
# @cache.memoize()
# def by_player(player_name):
#     player = Player.select().where(Player.ckey == player_name).first()
#     if not player:
#         abort(404)

#     pages = PaginatedQuery(player.rounds, 10)
#     return render_template("rounds/rounds.html", pages=pages, for_player=player_name)


# @bp.route("/rounds/winrates")
# @cache.cached(query_string=True)
# def recent_winrates():
#     colors_template = {
#         "Xeno": ("rgb(147,112,219)", "rgb(138,43,226)"),
#         "Marine": ("rgb(30,144,255)", "rgb(0,0,255)"),
#         "default": ("rgb(211,211,211)", "rgb(175,175,175)"),
#     }

#     colors = {}

#     where_clauses = []

#     # Mode query
#     mode = request.args.get("mode", None)  # Cap at 30, so we don't hammer a db
#     if mode:
#         where_clauses.append(Round.game_mode == mode)

#     # Date range
#     date_range = min(
#         30, int(request.args.get("limit", 7))
#     )  # Cap at 30, so we don't hammer a db
#     where_clauses.append(
#         Round.initialize_datetime > (datetime.now() - timedelta(days=date_range))
#     )

#     rounds = (
#         Round.select(Round.game_mode_result, Round.initialize_datetime)
#         .where(where_clauses)
#         .order_by(Round.id.desc())
#     )

#     game_results = set(
#         [r.game_mode_result for r in rounds if r.game_mode_result is not None]
#     )

#     date_range_iter = reversed(range(date_range))

#     today = date.today()
#     time_periods = [today - timedelta(days=day) for day in date_range_iter]
#     _debug_results = {"xeno": 0, "marine": 0}
#     day_results = {}
#     for result in game_results:
#         # Assign colours - need a better way
#         if result not in colors:
#             colors[result] = {}
#             if result.startswith("Xeno"):
#                 colors[result]["background"] = colors_template["Xeno"][0]
#                 colors[result]["border"] = colors_template["Xeno"][1]
#             elif result.startswith("Marine"):
#                 colors[result]["background"] = colors_template["Marine"][0]
#                 colors[result]["border"] = colors_template["Marine"][1]
#             else:
#                 colors[result]["background"] = colors_template["default"][0]
#                 colors[result]["border"] = colors_template["default"][1]

#         day_results[result] = {}
#         for period in time_periods:
#             wins = [
#                 1
#                 for r in rounds
#                 if r.game_mode_result == result
#                 and r.initialize_datetime.day == period.day
#             ]
#             day_results[result][period] = sum(wins)
#         _debug_results[result] = sum(
#             [1 for r in rounds if r.game_mode_result == result]
#         )
#         if result.startswith("Xeno"):
#             _debug_results["xeno"] += _debug_results[result]
#         if result.startswith("Marine"):
#             _debug_results["marine"] += _debug_results[result]
#     print(_debug_results)

#     return render_template(
#         "rounds/winrates.html",
#         labels=time_periods,
#         day_results=day_results,
#         colors=colors,
#     )
