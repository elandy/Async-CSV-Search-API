import pytest

from app.data_providers import VibraCSVDataProvider

# Fixture to provide a test CSV file path
@pytest.fixture
def test_csv_path(tmp_path):
    test_csv_file = tmp_path / 'test.csv'
    with open(test_csv_file, 'w') as f:
        f.write('1,John,Doe,john.doe@example.com,Male,Company1,New York\n')
        f.write('2,Jane,Smith,jane.smith@example.com,Female,Company2,Los Angeles\n')
        f.write('3,John,Second,john.second@example.com,Genderqueer,Company3,Buenos Aires\n')
    return test_csv_file


def test_vibra_csv_data_provider_adapt_search_terms(test_csv_path):
    """The adapt_search_terms should adapt the search dict to the columns of the vibra csv format"""
    # Arrange
    csv_data_provider = VibraCSVDataProvider(test_csv_path)
    search_terms = {'name': 'John', 'city': 'New York'}

    # Act
    adapted_search_terms = csv_data_provider.adapt_search_terms(search_terms)

    # Assert
    assert adapted_search_terms == {(1, 2): 'John', (6,): 'New York'}


def test_vibra_csv_data_provider_adapt_search_terms_empty_search_terms(test_csv_path):
    # Arrange
    csv_data_provider = VibraCSVDataProvider(test_csv_path)
    search_terms = {}

    # Act
    adapted_search_terms = csv_data_provider.adapt_search_terms(search_terms)

    # Assert
    assert adapted_search_terms == {}


def test_vibra_csv_data_provider_perform_search_no_results(test_csv_path):
    # Arrange
    csv_data_provider = VibraCSVDataProvider(test_csv_path)
    search_terms = {(1, 2): 'NonExistentName', (6,): 'NonExistentCity'}

    # Act
    results = csv_data_provider.perform_search(search_terms, quantity=None)

    # Assert
    assert len(results) == 0


def test_vibra_csv_data_provider_perform_search_quantity(test_csv_path):
    # Arrange
    csv_data_provider = VibraCSVDataProvider(test_csv_path)
    search_terms = {}

    # Act
    results = csv_data_provider.perform_search(search_terms, quantity=1)

    # Assert
    assert len(results) == 1


def test_vibra_csv_data_provider_perform_search_partial_match(test_csv_path):
    # Arrange
    csv_data_provider = VibraCSVDataProvider(test_csv_path)
    search_terms = {(1, 2): 'John', (6,): 'New'}

    # Act
    results = csv_data_provider.perform_search(search_terms, quantity=None)

    # Assert
    assert len(results) == 1
    assert results[0] == ['1', 'John', 'Doe', 'john.doe@example.com', 'Male', 'Company1', 'New York']


def test_vibra_csv_data_provider_perform_search(test_csv_path):
    # Arrange
    csv_data_provider = VibraCSVDataProvider(test_csv_path)
    search_terms = {(1, 2): 'John', (6,): 'New York'}

    # Act
    results = csv_data_provider.perform_search(search_terms, quantity=None)

    # Assert
    assert len(results) == 1
    assert results[0] == ['1', 'John', 'Doe', 'john.doe@example.com', 'Male', 'Company1', 'New York']