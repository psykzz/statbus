from flask import (
    Blueprint,
    abort,
    current_app,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from ..utils.tg_auth import Auth

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def ensure_tg_auth():
    if "tg_auth" not in g:
        key = current_app.config["SECRET_KEY"]
        g.tg_auth = Auth(key)


@bp.route("/")
def login():
    if "userinfo" in session:
        return redirect(url_for("personal.me"))

    # Create session
    redirect_uri = url_for(".callback", _external=True)
    tg_session = g.tg_auth.generate_session(redirect_uri)
    if tg_session is None:
        return {"error": "Unable to generate session"}
    session["auth.token"] = tg_session.session_private_token

    # Redirect for access
    return redirect(g.tg_auth.redirect(tg_session.session_public_token))


@bp.route("/logout")
def logout():
    session.clear()
    return {"status": "OK"}


@bp.route("/callback", methods=("GET", "POST"))
def callback():
    print(session, request)
    if "auth.token" not in session:
        session.clear()
        return {"error": "Invalid session state"}
    private_token = session["auth.token"]
    session["userinfo"] = g.tg_auth.get_user_data(private_token)

    return {"status": "OK"}
