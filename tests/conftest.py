import os

import pytest
import pandas as pd

from miner.app import App
from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.people import People

TEST_DATA_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/test_data"


@pytest.fixture(scope="session")
def tz():
    return "CET"


@pytest.fixture(scope="session")
def app():
    return App()


@pytest.fixture(scope="session")
def friends():
    return Friends(path=f"{TEST_DATA_PATH}/friends/friends.json")


@pytest.fixture(scope="session")
def conversations():
    yield Conversations(f"{TEST_DATA_PATH}")
    # tear-down
    os.remove(f"{TEST_DATA_PATH}/messages/inbox/private_messages.json")
    os.remove(f"{TEST_DATA_PATH}/messages/inbox/group_messages.json")


@pytest.fixture(scope="session")
def people(
    friends, conversations,
):
    def _get_people(name=None):
        return People(friends=friends, conversations=conversations)

    return _get_people()


@pytest.fixture(scope="session")
def analyzer(conversations, app):
    return MessagingAnalyzerManager(conversations, app._config)


@pytest.fixture(scope="session")
def panalyzer(analyzer):
    return analyzer.private


@pytest.fixture(scope="session")
def ganalyzer(analyzer):
    return analyzer.group


@pytest.fixture(scope="session")
def priv_stats(panalyzer):
    return panalyzer._stats


@pytest.fixture(scope="session")
def group_stats(ganalyzer):
    return ganalyzer._stats


@pytest.fixture(scope="session")
def sample_df():
    return pd.DataFrame(
        {"num_legs": [2, 4], "num_wings": [2, 0]}, index=["falcon", "dog"]
    )
