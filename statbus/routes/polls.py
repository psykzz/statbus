from datetime import datetime

from flask import Blueprint, render_template, request, abort
from playhouse.flask_utils import PaginatedQuery
from peewee import fn, JOIN

from statbus.database import PollQuestion, PollOption, PollVote, PollTextReply
from statbus.ext import cache

bp = Blueprint("polls", __name__)


@bp.route("/poll")
@bp.route("/polls")
@cache.cached()
def index():
    polls = PollQuestion.select().where(
        PollQuestion.adminonly == False, PollQuestion.dontshow == False
    )
    pages = PaginatedQuery(polls, 25)
    return render_template("polls/polls.html", pages=pages)


@bp.route("/poll/<int:poll_id>")
@cache.cached()
def detail(poll_id):
    poll = PollQuestion.select().where(PollQuestion.id == poll_id).first()
    if not poll or poll.is_hidden:
        abort(404)

    if poll.polltype == "OPTION":
        votes = (
            PollOption.select(PollOption.text, fn.Count(PollVote.id).alias("votes"))
            .join(PollVote, JOIN.LEFT_OUTER, on=(PollOption.id == PollVote.optionid))
            .where(PollVote.pollid == poll_id)
            .group_by(PollOption.text)
            .order_by(PollVote.optionid)
        )

        total = sum([x.votes for x in votes])
        percentages = ["{0:.2f}".format((int(x.votes) / total) * 100) for x in votes]

        return render_template(
            "polls/detail_option.html",
            current_poll=poll,
            votes=votes,
            percentages=percentages,
            datetime=datetime,
        )

    elif poll.polltype == "TEXT":
        return render_template("polls/detail_text.html", poll=poll)

    elif poll.polltype == "NUMVAL":
        return render_template("polls/detail_numval.html", poll=poll)

    elif poll.polltype == "MULTICHOICE":
        return render_template("polls/detail_multichoice.html", poll=poll)

    elif poll.polltype == "IRV":
        return render_template("polls/detail_irv.html", poll=poll)

    return abort(404)
