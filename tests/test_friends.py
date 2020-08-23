import pytest
import os
import pandas as pd

from miner import utils

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


# TODO what happens when two friends have same name??
@pytest.fixture()
def expected_friends():
    return {'John Doe': {'compact_name': 'johndoe'},
            'Donald Duck': {'compact_name': 'donaldduck'},
            'Szett Droxler': {'compact_name': 'szettdroxler'},
            'Foo Bar': {'compact_name': 'foobar'},
            'Tőke Hal': {'compact_name': 'tokehal'},
            'Dér Dénes': {'compact_name': 'derdenes'},
            'Teflon Musk': {'compact_name': 'teflonmusk'},
            'Daisy Duck': {'compact_name': 'daisyduck'},
            'Guy Fawkes': {'compact_name': 'guyfawkes'}}


def test_data_is_df(friends):
    assert isinstance(friends.data, pd.DataFrame)


def test_data_is_right_length(friends):
    assert len(friends.data) == 9


def test_has_expected_columns(friends):
    assert list(friends.data.columns) == ['name']


def test_has_expected_names(friends, expected_friends):
    assert all([p in expected_friends for p in friends.data.name])


def test_has_metadata(friends):
    assert friends.metadata is not None


def test_metadata_len(friends):
    assert friends.metadata.length is 9


def test_metadata_path(friends):
    assert 'friends/friends.json' in friends.metadata.path


def test_has_preprocessors(friends):
    assert friends.preprocessor is not None
