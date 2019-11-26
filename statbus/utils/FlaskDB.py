from flask import request
from playhouse.flask_utils import FlaskDB


class FlaskDBWrapper(FlaskDB):
    """Custom handler here to avoid connecting for static files"""

    def connect_db(self):
        if request.endpoint in ("static",):
            return
        self.database.connect()
