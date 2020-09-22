import pytest
import os

from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.message.conversations import Conversations
from miner.app import App
from miner.people import People
from miner.data import FacebookData
from miner.friends import Friends

TEST_DATA_PATH = f"{os.getcwd()}/test_data"


@pytest.fixture(scope="session")
def app():
    return App(TEST_DATA_PATH)


@pytest.fixture(scope="session")
def friends():
    return Friends(path=f"{TEST_DATA_PATH}/friends/friends.json")


@pytest.fixture(scope="session")
def conversations():
    return Conversations(f"{TEST_DATA_PATH}")


@pytest.fixture(scope="session")
def get_people(
    friends, conversations,
):
    def _get_people(name=None):
        return People(friends=friends, conversations=conversations)

    return _get_people


@pytest.fixture(scope="function")
def facebook_data():
    def _facebook_data(sub_path=""):
        return FacebookData(path=TEST_DATA_PATH + sub_path)

    return _facebook_data


@pytest.fixture(scope="session")
def analyzer(conversations, app):
    return MessagingAnalyzerManager(conversations, app._config)


@pytest.fixture(scope="session")
def priv_msg_analyzer(analyzer):
    return analyzer.private


@pytest.fixture(scope="session")
def group_msg_analyzer(analyzer):
    return analyzer.group
