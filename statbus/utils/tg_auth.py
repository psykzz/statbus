import base64
import requests
import urllib


class Auth(object):
    __slots__ = ["api", "private_site_key"]

    def __init__(self, private_site_key):
        self.api = requests.Session()
        self.private_site_key = base64.b64encode(private_site_key).decode("utf-8")

    def generate_session(self, redirect_uri):
        api_res = self.api.get(
            f"https://tgstation13.org/phpBB/oauth_create_session.php?site_private_token={self.private_site_key}&return_uri={redirect_uri}"
        ).json()

        if api_res.get("status") != "OK":
            return
        return Session.from_data(api_res)

    def redirect(self, public_token):
        return f"https://tgstation13.org/phpBB/oauth.php?session_public_token={public_token}"

    def get_user_data(self, session_private_token):
        print(
            f"https://tgstation13.org/phpBB/oauth_get_session_info.php?site_private_token={self.private_site_key}&session_private_token={session_private_token}"
        )
        api_res = self.api.get(
            f"https://tgstation13.org/phpBB/oauth_get_session_info.php?site_private_token={self.private_site_key}&session_private_token={session_private_token}"
        ).json()
        return api_res


class Session(object):
    __slots__ = ["session_public_token", "session_private_token"]

    @classmethod
    def from_data(cls, data):
        session = cls()
        session.session_public_token = urllib.parse.quote(
            data.get("session_public_token", "")
        )
        session.session_private_token = urllib.parse.quote(
            data.get("session_private_token", "")
        )
        return session
