import pandas as pd
import pytest
import os

from miner.Conversation import Conversation
from miner import utils

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


@pytest.fixture(scope='session')
def convo():
    return Conversation(path=f'{TEST_DATA_PATH}/messages/inbox/tokehal_sdf7fs9d876/message_1.json')


def test_data_is_df(convo):
    assert isinstance(convo.data, pd.DataFrame)


def test_data_has_right_length(convo):
    assert len(convo.data) == 5


def test_metadata_has_fields(convo):
    expected_fields = ['is_still_participant', 'media_dir', 'participants', 'thread_path', 'thread_type', 'title']
    for field in expected_fields:
        assert hasattr(convo.metadata, field)
