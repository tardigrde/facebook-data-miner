import pytest
import os

from miner.People import People
from miner.FacebookData import FacebookData

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


@pytest.fixture(scope='session')
def get_people():
    def _get_people(name=None):
        return People(path=TEST_DATA_PATH, name=name)
    return _get_people

@pytest.fixture(scope='function')
def facebook_data():
    def _facebook_data(sub_path=''):
        return FacebookData(path=TEST_DATA_PATH+sub_path)
    return _facebook_data


