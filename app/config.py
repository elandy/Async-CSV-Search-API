import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "hard-to-guess")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
    REDIS_SEARCH_QUEUE = os.getenv("SEARCH_QUEUE", "search_queue")


class Development(Config): ...


class Production(Config): ...


class Test(Config):
    TESTING = True
    DEBUG = True
    REDIS_URL = "redis://localhost:6379/1"


CONFIG_MAP = {"development": Development, "production": Production, "testing": Test}
