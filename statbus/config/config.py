from dotenv import load_dotenv

load_dotenv()

import os
import tempfile
import redis

DATABASE = {
    "engine": "peewee.MySQLDatabase",
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", 3306)),
    "name": os.getenv("DATABASE_NAME", "tgmc"),
    "user": os.getenv("DATABASE_USER", "root"),
    "passwd": os.getenv("DATABASE_PASSWORD", "password"),
}

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = os.urandom(64)
else:
    SECRET_KEY = SECRET_KEY.encode("utf-8")


## caching
CACHE_TYPE = "filesystem"
CACHE_DEFAULT_TIMEOUT = 60
CACHE_DIR = tempfile.mkdtemp()

## Session
SESSION_TYPE = "filesystem"
SESSION_FILE_DIR = tempfile.mkdtemp()

## Redis
# If we have redis available we can change our cache type from filesystem
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    REDIS_CLIENT = redis.from_url(REDIS_URL)
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = REDIS_URL
    SESSION_TYPE = "redis"
    SESSION_REDIS = REDIS_CLIENT


## Social links
SOCIAL_LINK_GITHUB = os.getenv(
    "SOCIAL_LINK_GITHUB", "https://github.com/tgstation/TerraGov-Marine-Corps"
)
SOCIAL_LINK_PLAYNOW = os.getenv(
    "SOCIAL_LINK_PLAYNOW", "byond://tgmc.tgstation13.org:5337"
)
SOCIAL_LINK_DISCORD = os.getenv("SOCIAL_LINK_DISCORD", "https://discord.gg/2dFpfNE")
SOCIAL_LINK_GETTING_STARTED = os.getenv(
    "SOCIAL_LINK_GETTING_STARTED", "https://tgstation13.org/wiki/TGMC"
)


## Github Token
GITHUB_REPO = os.getenv("GITHUB_REPO", "tgstation/TerraGov-Marine-Corps")
GITHUB_LABELS = os.getenv("GITHUB_LABELS", "Needs Balance Review,Balance/Rebalance")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
