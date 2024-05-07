from unittest.mock import patch

import pytest
from fakeredis import FakeStrictRedis

from app import create_app
from app.config import Test as TestConfig


@pytest.fixture(scope='session')
def redis_patch():
    with patch('redis.StrictRedis.from_url', return_value=FakeStrictRedis()) as patched:
        yield patched


@pytest.fixture()
def app(redis_patch):
    app = create_app(TestConfig)
    app.redis = redis_patch
    with app.app_context():
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://',
        'result_backend': 'redis://'
    }
