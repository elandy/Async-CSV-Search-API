from app.tasks import process_search


def test_process_search(client):
    task_id = '123'
    search_params = {}
    quantity = None
    result = process_search.apply(args=(task_id, search_params, quantity)).get()
    assert result == task_id

