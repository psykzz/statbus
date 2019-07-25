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


@bp.before_app_request
def ensure_tg_auth():
    if "tg_auth" not in g:
        key = current_app.config["SECRET_KEY"].encode("utf-8")
        g.tg_auth = Auth(key)


@bp.route("/")
def index():
    # Create session
    redirect_uri = url_for(".callback", _external=True)
    print(redirect_uri)
    tg_session = g.tg_auth.generate_session(redirect_uri)
    if tg_session is None:
        return redirect(url_for(".error"))
        print(tg_session)
    session["auth.token"] = tg_session.session_private_token
    # Redirect for access
    return redirect(g.tg_auth.redirect(tg_session.session_public_token))


@bp.route("/callback", methods=("GET", "POST"))
def callback():
    if "auth.token" not in session:
        session.clear()
        redirect(".index")
    private_token = session["auth.token"]
    session["userinfo"] = g.tg_auth.get_user_data(private_token)

    return redirect(url_for(".userinfo"))


@bp.route("/userinfo")
def userinfo():
    return jsonify(session["userinfo"])


@bp.route("/error")
def error():
    return "error"


"""

app = Flask(__name__)
app.secret_key = b'not that secret'
app.config.from_object(__name__)

tg_private_token = base64.urlsafe_b64encode(b"A really secret character set of thingsa").decode('ascii')


@app.route('/')
def index():
  return "click to <a href='/login'>login</a>"

@app.route('/login')
def login():
  print(tg_private_token)
  redirect_uri = url_for('callback', _external=True)
  print(redirect_uri)
  api_res = api.get(f'https://tgstation13.org/phpBB/oauth_create_session.php?site_private_token={tg_private_token}&return_uri={redirect_uri}').json()
  print(api_res)
  if api_res.get('status') != "OK":
      return redirect('/')

  public_token = api_res.get('session_public_token')
  session['oauth_token'] = api_res.get('session_private_token')

  return redirect(f'https://tgstation13.org/phpBB/oauth.php?session_public_token={public_token}')

@app.route('/callback')
def callback():
  private_token = session['oauth_token']
  response = api.get(f'https://tgstation13.org/phpBB/oauth_get_session_info.php?site_private_token={tg_private_token}&session_private_token={SomeTokenHere}').json()
  if response.status!= "OK":
      return redirect('/')
  return "OK"

def get_user():
  data = {}
  return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    """
