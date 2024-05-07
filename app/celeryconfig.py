import os

# Task broker and results backend settings.
broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/1")
result_backend = broker_url

# List of modules to import when the Celery worker starts.
imports = ("app.tasks",)

task_routes = {"app.tasks.process_search": {"queue": "search_queue"}}

task_ignore_result = True
CSV_FILE_PATH = os.path.join("app", "data", "vibra_challenge.csv")