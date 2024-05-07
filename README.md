# Async CSV Search API


## Prerequisites

- Python 3.11+

- Poetry

- Docker and docker compose

## Main features

This is an asynchronous CSV search API built with Flask and Celery, using Redis as the broker and result backend.

### Search Endpoint: 
Allows users to enqueue a search task by providing search parameters such as name and city.
    
    curl -X GET 'http://localhost:5000/search?name=John&city=New%20York&quantity=10'

### Result Endpoint: 
Allows users to check the status or retrieve the result of a search task using a task ID.

    curl -X GET 'http://localhost:5000/search_result/task_id'

### Extensible ResultsService with Multiple DataProviders
The Async CSV Search API utilizes an extensible ResultsService that allows for the management of multiple DataProviders. This design enables the API to easily incorporate new data sources or change existing ones without requiring significant modifications to the core functionality.

### DataProviders
VibraCSVDataProvider: This DataProvider is specifically designed to handle CSV files with a format similar to vibra_challenge.csv. It implements methods to adapt search terms and perform searches based on the provided criteria.
ResultsService
The ResultsService class orchestrates the search process by aggregating results from different DataProviders. It allows for a flexible and scalable approach to searching, making it easy to integrate new search strategies or data sources.

### Redis Expiring Keys for Temporary Results Storage
To manage search results efficiently, the API uses Redis expiring keys. When a search task is enqueued, the API stores the task ID and the search results in Redis with a specified expiration time. This approach ensures that search results are automatically deleted from Redis after a certain period, reducing the risk of storing outdated or unnecessary data.




## Common tasks

### Create virtual environment with dependencies

    python3 -m venv venv && source venv/bin/activate && poetry install

### Specify development config (with debug mode on)

    export FLASK_ENV=development

### Run development flask server

    flask run

### Run development gunicorn server with aiohttp worker

    gunicorn -b :5000 aioapp:aioapp -k aiohttp.worker.GunicornWebWorker --reload

## Run celery

    celery -A app.tasks worker -Q search_queue --loglevel=INFO

### Run production gunicorn server

    ./boot.sh

### Build docker image

    docker build .

### Run with docker compose

    docker-compose up --build

### Format Python code with black

    black . --exclude venv

### Run git pre-commit hooks

    pre-commit run --all-files
