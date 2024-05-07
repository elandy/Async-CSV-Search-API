from unittest.mock import MagicMock

from app.data_providers import ResultsService


def test_results_service_empty_data_providers():
    """Test that the search returns no results if it has no data providers"""
    # Arrange
    results_service = ResultsService([])

    # Act
    search_results = results_service.search({}, quantity=None)

    # Assert
    assert len(search_results) == 0


def test_results_service_single_data_provider():
    """Test that the search returns the John from one data providers"""
    # Arrange
    mock_data_provider = MagicMock()
    mock_data_provider.search.return_value = [{'id': 1, 'name': 'John', 'city': 'New York'}]
    results_service = ResultsService([mock_data_provider])

    # Act
    search_results = results_service.search({'name': 'John', 'city': 'New York'}, quantity=None)

    # Assert
    assert len(search_results) == 1
    assert search_results[0]['id'] == 1
    assert search_results[0]['name'] == 'John'
    assert search_results[0]['city'] == 'New York'


def test_results_service_multiple_data_providers():
    """Test that the search returns the Johns from all data providers"""
    # Arrange
    mock_data_provider1 = MagicMock()
    mock_data_provider1.search.return_value = [{'id': 1, 'name': 'John', 'city': 'New York'}]
    mock_data_provider2 = MagicMock()
    mock_data_provider2.search.return_value = [{'id': 2, 'name': 'John', 'city': 'Los Angeles'}]
    results_service = ResultsService([mock_data_provider1, mock_data_provider2])

    # Act
    search_results = results_service.search({'name': 'John'}, quantity=None)

    # Assert
    assert len(search_results) == 2
    assert search_results[0]['id'] == 1
    assert search_results[0]['name'] == 'John'
    assert search_results[0]['city'] == 'New York'
    assert search_results[1]['id'] == 2
    assert search_results[1]['name'] == 'John'
    assert search_results[1]['city'] == 'Los Angeles'
