# from datetime import date, datetime, timedelta

# from flask import Blueprint, render_template, request, abort
# from playhouse.flask_utils import PaginatedQuery

# from statbus.models.player import Player
# from statbus.models.round import Round
# from statbus.ext import cache
# from statbus.utils import github


# bp = Blueprint("rounds", __name__)


# def rolling_win_rates(game_states, rounds, period=7, granular_hours=24):
#     results = {}
#     now = date.today()

#     tmpl = {}
#     for state in game_states:
#         tmpl[state] = -1
#     for window in range(period):
#         results[window] = tmpl.copy()

#     print(results)


# @bp.route("/round")
# @bp.route("/rounds")
# @cache.cached()
# def index():
#     rounds = Round.select().order_by(Round.id.desc())
#     pages = PaginatedQuery(rounds, 10)
#     return {"pages": pages.page}
#     # return render_template("rounds/rounds.html", pages=pages)


# @bp.route("/rounds/<int:round_id>")
# @cache.memoize()
# def detail(round_id):
#     print(datetime.now())
#     round_info = Round.select().where(Round.id == round_id).first()
#     if not round_info or not round_info.end_datetime:
#         abort(404)

#     print(datetime.now())

#     pr_list = round_info.merged_prs.values()
#     print(datetime.now())
#     balance_prs = github.get_balance_prs(pr_list)
#     print(datetime.now())

#     return render_template(
#         "rounds/round_info.html", round_info=round_info, balance_prs=balance_prs
#     )


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
