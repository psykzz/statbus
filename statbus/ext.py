from flask_caching import Cache

cache = Cache()


from flask_session import Session

session = Session()


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from flask_cors import CORS

cors = CORS()
