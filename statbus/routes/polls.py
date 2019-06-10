from flask import Blueprint, render_template, request

bp = Blueprint('polls', __name__)

@bp.route("/")
def index():
	return render_template('index.html')


@bp.route("/poll", methods=("GET",))
def poll():
	offset = request.args.get('offset')

	return render_template('poll.html', offset=offset)


@bp.route("/poll/<int:poll_id>")
def pollid(poll_id=None):

	return render_template('pollid.html', poll_id=poll_id)


