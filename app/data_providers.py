import csv
from abc import ABC, abstractmethod
from enum import Enum

from celery.utils.log import get_task_logger
LOGGER = get_task_logger(__name__)


class ResultsService:
    def __init__(self, data_providers):
        self.data_providers = data_providers

    def search(self, search_terms: dict[str, str], quantity=None):
        results = []
        for data_provider in self.data_providers:
            data_provider_results = data_provider.search(search_terms, quantity)
            results.extend(data_provider_results)
            if quantity and len(results) >= quantity:
                break
        return results


class DataProvider(ABC):
    def search(self, search_terms: dict[str, str], quantity=None):
        """Search template"""
        search_terms = self.adapt_search_terms(search_terms)
        results = self.perform_search(search_terms, quantity)
        return results

    def adapt_search_terms(self, search_terms: dict[str, str]):
        """Default behavior is to return the search_term dict as is
        Subclasses must override this if special adaptation is needed"""
        return search_terms

    @abstractmethod
    def perform_search(self, search_terms, quantity):
        pass


class VibraCSVDataProvider(DataProvider):
    """This is a data provider that deals exclusively with csv files with the format of the vibra_challenge.csv file"""
    class ColumnNames(Enum):
        ID = 'id'
        FIRST_NAME = 'first_name'
        LAST_NAME = 'last_name'
        EMAIL = 'email'
        GENDER = 'gender'
        COMPANY = 'company'
        CITY = 'city'

    # what data each column of the csv holds
    column_map = {ColumnNames.ID: 0,
                  ColumnNames.FIRST_NAME: 1,
                  ColumnNames.LAST_NAME: 2,
                  ColumnNames.EMAIL: 3,
                  ColumnNames.GENDER: 4,
                  ColumnNames.COMPANY: 5,
                  ColumnNames.CITY: 6}

    # search terms can look into more than one field
    # if we need tu support new search terms, they should be added here
    search_term_map = {'name': (ColumnNames.FIRST_NAME, ColumnNames.LAST_NAME),
                       'city': (ColumnNames.CITY,)}
    
    def __init__(self, csv_path):
        self.csv_path = csv_path

    def adapt_search_terms(self, search_terms: dict[str, str]):
        # remove unsupported search terms
        for search_term in list(search_terms.keys()):
            if search_term not in self.search_term_map.keys():
                del search_terms[search_term]

        # build new search_term dict with lists of column indexes. Converts:
        # {'name': 'John'} -> {[1, 2]: 'John'}

        column_list_search_terms = {}
        for key, value in search_terms.items():
            col_names = self.search_term_map[key]
            column_numbers_for_term = tuple(self.column_map[col_name] for col_name in col_names)
            column_list_search_terms[column_numbers_for_term] = value

        print(column_list_search_terms)

        return column_list_search_terms

    def perform_search(self, search_terms: dict[tuple[int], str], quantity):
        try:
            with open(self.csv_path, mode="r") as file:
                csv_reader = csv.reader(file)
                results = []
                for row in csv_reader:
                    if self.row_matches(row, search_terms):
                        results.append(row)
                    if quantity and quantity == len(results):
                        break
            return results
        except FileNotFoundError:
            LOGGER.error(f"File {self.csv_path} not found.")
        except csv.Error as e:
            LOGGER.error(f"Error reading CSV file: {e}")
        return []

    @staticmethod
    def row_matches(row, search_terms):
        for columns, value in search_terms.items():
            # if value was not found in any of the columns, row doesn't match
            if all(value.lower() not in row[col].lower() for col in columns):
                return False
        return True
