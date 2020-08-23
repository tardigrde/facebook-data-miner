import pytest
import os

from miner.message.conversation_analyzer import ConversationAnalyzer
from miner.message.conversations import Conversations
from miner.people import People
from miner.data import FacebookData
from miner.friends import Friends

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


@pytest.fixture(scope='session')
def friends():
    return Friends(path=f'{TEST_DATA_PATH}/friends/friends.json')


@pytest.fixture(scope='session')
def conversations():
    return Conversations(f'{TEST_DATA_PATH}')


@pytest.fixture(scope='session')
def get_people(friends, conversations, ):
    def _get_people(name=None):
        return People(friends=friends, conversations=conversations)

    return _get_people


@pytest.fixture(scope='function')
def facebook_data():
    def _facebook_data(sub_path=''):
        return FacebookData(path=TEST_DATA_PATH + sub_path)

    return _facebook_data


@pytest.fixture(scope='session')
def analyzer(conversations):
    return ConversationAnalyzer(conversations)
