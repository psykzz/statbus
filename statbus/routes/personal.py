# from datetime import datetime, timedelta

# from flask import Blueprint, render_template, request, abort, session, g
# from playhouse.flask_utils import PaginatedQuery

# from statbus.models.player import Player
# from statbus.models.message import Messages
# from statbus.models.round import Round
# from statbus.ext import cache
# from statbus.utils import github


# bp = Blueprint("personal", __name__)


# @bp.before_request
# def before_req():
#     player_name = session.get("userinfo", {}).get("byond_ckey")
#     if not player_name:
#         abort(401)
#     player = Player.select().where(Player.ckey == player_name).first()
#     if not player:
#         player = Player()
#         player.ckey = player_name
#         player.byond_key = player_name
#     g.player = player


# @bp.route("/me")
# @cache.cached()
# def me():
#     return render_template("personal/personal.html", player=g.player)


# @bp.route("/me/notes")
# @cache.cached()
# def notes():
#     return render_template("personal/personal.html", player=g.player)


# @bp.route("/me/rounds")
# @cache.cached()
# def rounds():
#     return render_template("personal/personal.html", player=g.player)
