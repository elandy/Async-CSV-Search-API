import json
import os
from time import sleep

from celery import Celery
from celery.utils.log import get_task_logger
import redis

from app.config import Config
from app.data_providers import VibraCSVDataProvider, ResultsService

config = Config()
redis_client = redis.StrictRedis.from_url(config.REDIS_URL)

LOGGER = get_task_logger(__name__)
APP_NAME = "app.tasks"

# adjust this value to control how long search results are kept on redis
SEARCH_RESULT_EXPIRE_SECONDS = 10

try:
    app = Celery(APP_NAME)
    app.config_from_object("app.celeryconfig", force=True)
except ImportError:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/1")
    print(f"celeryconfig not found, using {redis_url}")
    app = Celery(APP_NAME, broker=redis_url, backend=redis_url)


@app.task(bind=True)
def process_search(self, task_id, search_params, quantity):
    # Process the search
    csv_data_provider = VibraCSVDataProvider(app.conf.CSV_FILE_PATH)
    results_service = ResultsService([csv_data_provider])
    store_result(task_id, results_service.search(search_params, quantity=quantity))
    return task_id


def store_result(task_id, result):
    retries = 3
    while retries > 0:
        try:
            redis_client.set(task_id, json.dumps(result))
            redis_client.expire(task_id, SEARCH_RESULT_EXPIRE_SECONDS)
            return  # Success, exit the loop
        except ConnectionError:
            retries -= 1
            sleep(1)  # Wait for a second before retrying
    # All retries failed, handle the failure
    LOGGER.error(f"Could not connect to redis for storing the result")
