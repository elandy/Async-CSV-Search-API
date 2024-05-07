import uuid
from time import sleep

from apiflask import APIBlueprint as Blueprint
from flask import current_app as app
from flask import jsonify, request

from app import tasks
from app.errors.handlers import error_response

bp = Blueprint("main", __name__)


@bp.route("/error/<int:code>")
def error(code):
    app.logger.error(f"Error: {code}")
    return error_response(code)


@bp.route("/search", methods=["GET"])
def enqueue_search():
    # Currently we allow hitting this endpoint without parameters. This returns all the data
    # It can be prevented by adding validation here
    name = request.args.get("name")
    city = request.args.get("city")
    try:
        quantity = int(request.args.get("quantity"))
    except ValueError:
        quantity = None
    except TypeError:
        quantity = None

    search_params = build_search_param_dict(name, city)

    task_id = str(uuid.uuid4())
    tasks.process_search.apply_async(args=[task_id, search_params, quantity])
    return jsonify({"message": "Search enqueued successfully", "task_id": task_id}), 200


def build_search_param_dict(name, city):
    search_params = {}
    for var_name, var_value in [('name', name), ('city', city)]:
        if var_value:
            search_params[var_name] = var_value
    return search_params


@bp.route("/search_result/<task_id>", methods=["GET"])
def get_task_result(task_id):
    # Check if the result is available in Redis
    # With getdel, the result can be retrieved only once
    # This can be changed to get, and the result can be retrieved many times until
    # the redis key expires
    retries = 3
    while retries > 0:
        try:
            result = app.redis.get(task_id)
            if result:
                return jsonify({"task_id": task_id, "result": result.decode()}), 200
            else:
                return jsonify({"task_id": task_id, "status": "processing"}), 202
        except ConnectionError:
            retries -= 1
            sleep(1)  # Wait for a second before retrying
    return jsonify({"task_id": task_id, "status": "error"}), 500  # All retries failed, return an error status
