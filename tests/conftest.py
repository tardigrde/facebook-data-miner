import pytest
from People import People

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


@pytest.fixture(scope='session')
def people():
    p = People(path=TEST_DATA_PATH)
    return p
