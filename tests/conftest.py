import os

import pytest
import pandas as pd

from miner.app import App
from miner.friends import Friends
from miner.message.conversations import Conversations
from miner.message.messaging_analyzer import MessagingAnalyzerManager
from miner.people import People
from miner.utils import const

TEST_DATA_PATH = (
    f"{os.path.dirname(os.path.realpath(__file__))}" f"{os.sep}test_data"
)


@pytest.fixture(scope="session")
def DATA_PATH():
    return TEST_DATA_PATH


@pytest.fixture(scope="session")
def app():
    return App(path=TEST_DATA_PATH)


@pytest.fixture(scope="session")
def friends():
    return Friends(path=os.path.join(TEST_DATA_PATH, *const.FRIENDS_PATH))


@pytest.fixture(scope="session")
def conversations():
    yield Conversations(f"{TEST_DATA_PATH}")
    # tear-down
    os.remove(
        os.path.join(
            TEST_DATA_PATH, *const.MESSAGES_SUBPATH, "private_messages.json"
        )
    )
    os.remove(
        os.path.join(
            TEST_DATA_PATH, *const.MESSAGES_SUBPATH, "group_messages.json"
        )
    )


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
def people(
    friends,
    conversations,
):
    def _get_people(name=None):
        return People(friends=friends, conversations=conversations)

    return _get_people()


@pytest.fixture(scope="session")
def sample_df():
    return pd.DataFrame(
        {"num_legs": [2, 4], "num_wings": [2, 0]}, index=["falcon", "dog"]
    )


@pytest.fixture(scope="session")
def tz_name():
    return "UTC"
