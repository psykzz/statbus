from flask import (
    Blueprint,
    render_template,
    request,
    current_app,
    g,
    url_for,
    redirect,
    session,
    jsonify,
)
from ..utils.tg_auth import Auth

bp = Blueprint("auth", __name__, url_prefix="/auth")


def require_auth(redirect=None):
    def inner(f):
        # if "auth.token" not in session:
        #     if redirect:
        #         return redirect(url_for(endpoint))
        #     else:
        #         return abort(401)
        f()

    return inner


@bp.before_app_request
def ensure_tg_auth():
    if "tg_auth" not in g:
        key = current_app.config["SECRET_KEY"]
        g.tg_auth = Auth(key)


@bp.route("/")
def login():
    if "auth.token" in session:
        return redirect(url_for(".userinfo"))
    # Create session
    redirect_uri = url_for(".callback", _external=True)
    tg_session = g.tg_auth.generate_session(redirect_uri)
    if tg_session is None:
        return redirect(url_for(".error"))
    session["auth.token"] = tg_session.session_private_token
    # Redirect for access
    return redirect(g.tg_auth.redirect(tg_session.session_public_token))


@bp.route("/callback", methods=("GET", "POST"))
def callback():
    if "auth.token" not in session:
        session.clear()
        return redirect(".login")
    private_token = session["auth.token"]
    session["userinfo"] = g.tg_auth.get_user_data(private_token)

    return redirect(url_for(".userinfo"))


@bp.route("/userinfo")
def userinfo():
    return jsonify(session["userinfo"])


@bp.route("/error")
def error():
    return "error"
