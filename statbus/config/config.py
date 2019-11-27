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

SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(64)).encode('utf-8')

## caching
CACHE_TYPE = "filesystem"
CACHE_DEFAULT_TIMEOUT = 1
CACHE_DIR = tempfile.mkdtemp()

## Session
SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = tempfile.mkdtemp()


## Social links
SOCIAL_LINK_GITHUB = os.getenv('SOCIAL_LINK_GITHUB', 'https://github.com/tgstation/TerraGov-Marine-Corps')
SOCIAL_LINK_DISCORD = os.getenv('SOCIAL_LINK_DISCORD', 'https://discord.gg/2dFpfNE')
SOCIAL_LINK_GETTING_STARTED = os.getenv('SOCIAL_LINK_GETTING_STARTED', 'https://tgstation13.org/wiki/TGMC')