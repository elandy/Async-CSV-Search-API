import redis
from apiflask import APIFlask as Flask

from .config import CONFIG_MAP
from .logger import get_handler
from dotenv import load_dotenv


def create_app(config=None):
    load_dotenv()
    # read config
    app = Flask(__name__)

    if app.config.get("ENV") is None:
        app.config["ENV"] = "development"

    if config is None:
        config = CONFIG_MAP[app.config["ENV"]]

    app.config.from_object(config)

    # add customized plugin
    app.redis = redis.StrictRedis.from_url(config.REDIS_URL)

    # import blueprints
    from app.errors import bp as errors_bp
    from app.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(main_bp)

    return app
