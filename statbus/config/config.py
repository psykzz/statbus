from dotenv import load_dotenv

load_dotenv()

import os
import tempfile

DATABASE = {
    "engine": "peewee.MySQLDatabase",
    "host": os.getenv("DATABASE_HOST", "localhost"),
    "port": int(os.getenv("DATABASE_PORT", 3306)),
    "name": os.getenv("DATABASE_NAME", "tgmc"),
    "user": os.getenv("DATABASE_USER", "root"),
    "passwd": os.getenv("DATABASE_PASSWORD", "password"),
}

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(64))

## caching
CACHE_TYPE = "filesystem"
CACHE_DEFAULT_TIMEOUT = 300
CACHE_DIR = tempfile.mkdtemp()

## Session
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = tempfile.mkdtemp()

