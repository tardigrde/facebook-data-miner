import pytest
import os

from miner.FacebookData import FacebookData
from miner import utils

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


@pytest.fixture
def friends(facebook_data):
    return facebook_data('/friends/friends.json')


def test_read_data(friends):
    friends.read_data(utils.read_json)
    raw_data = friends.raw_data
    assert isinstance(raw_data, dict)
    assert raw_data.get('friends')
    assert len(raw_data.get('friends'))


def test_preprocess_without_read_data(friends):
    with pytest.raises(SystemExit):
        friends.preprocess([int])


def test_preprocess_without_callable(friends):
    friends.read_data(utils.read_json)
    with pytest.raises(SystemExit):
        friends.preprocess([('this is a string, not a callable', None)])
