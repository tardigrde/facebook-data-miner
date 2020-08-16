import pytest
import os

from miner.People import People

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


@pytest.fixture(scope='session')
def get_people():
    def _get_people(name=None):
        return People(path=TEST_DATA_PATH, name=name)
    return _get_people

