import pytest
from miner.People import People

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


@pytest.fixture(scope='session')
def get_people():
    def _get_people(name=None):
        return People(path=TEST_DATA_PATH, name=name)
    return _get_people

