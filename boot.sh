#!/bin/sh
exec $HOME/.local/bin/poetry run gunicorn -b :5000 --access-logfile - --error-logfile - aioapp:aioapp -k aiohttp.worker.GunicornWebWorker &
exec $HOME/.local/bin/poetry run celery -A app.tasks worker -Q search_queue --loglevel=INFO
