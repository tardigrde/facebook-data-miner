import pytest
import os
import pandas as pd

from miner.Friends import Friends
from miner import utils

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


# TODO what happens when two friends have same name??
@pytest.fixture()
def expected_friends():
    return {'John Doe': {'compact_name': 'johndoe', 'path': None},
            'Donald Duck': {'compact_name': 'donaldduck', 'path': None},
            'Szett Droxler': {'compact_name': 'szettdroxler', 'path': None},
            'Foo Bar': {'compact_name': 'foobar', 'path': None},
            'Tőke Hal': {'compact_name': 'tokehal', 'path': None},
            'Dér Dénes': {'compact_name': 'derdenes', 'path': None},
            'Teflon Musk': {'compact_name': 'teflonmusk', 'path': None},
            'Daisy Duck': {'compact_name': 'daisyduck', 'path': None},
            'Guy Fawkes': {'compact_name': 'guyfawkes', 'path': None}}


@pytest.fixture(scope='session')
def friends():
    return Friends(path=TEST_DATA_PATH)


def test_data_is_df(friends):
    assert isinstance(friends.data, pd.DataFrame)


def test_data_is_right_length(friends):
    assert len(friends.data) == 9


def test_has_expected_columns(friends):
    assert list(friends.data.columns) == ['name', 'timestamp']


def test_has_expected_names(friends, expected_friends):
    assert all([p in expected_friends for p in friends.data.name])

# @pytest.fixture()
# def friends():
#     f = Friends(f'{TEST_DATA_PATH}/friends/friends.json')
#     return f.get_people()
#
#
# def test_get_peoples_names_from_friends(friends, expected_friends):
#     assert all([p in expected_friends.keys() for p in friends])
#
#
# def test_get_peoples_compact_name_from_friends(friends, expected_friends):
#     expected_compact_names = [value.get('compact_name') for value in expected_friends.values()]
#
#     assert all([p.compact_name in expected_compact_names for p in friends.values()])
