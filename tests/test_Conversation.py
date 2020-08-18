import pandas as pd
import pytest
import os

from miner.Conversation import Conversation
from miner import utils

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


@pytest.fixture(scope='session')
def convo():
    return Conversation(path=TEST_DATA_PATH, msgs_dir='/tokehal_sdf7fs9d876/message_1.json')

def test_data_is_df(convo):
    assert isinstance(convo.data, pd.DataFrame)

def test_data_has_right_length(convo):
    assert len(convo.data)
