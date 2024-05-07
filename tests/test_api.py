from unittest.mock import MagicMock
from app.tasks import process_search


def test_enqueue_search(client, app):
    response = client.get('/search')
    assert response.status_code == 200
    assert response.json['message'] == 'Search enqueued successfully'
    assert 'task_id' in response.json


def test_process_search(app):
    mock_csv_data_provider = MagicMock()
    mock_results_service = MagicMock()
    mock_results_service.search.return_value = [{'id': 1, 'name': 'John', 'city': 'New York'}]
    mock_csv_data_provider.return_value = mock_results_service
    task = process_search.apply(args=[1, {'name': 'John', 'city': 'New York'}, 10])
    assert task.status == 'SUCCESS'
