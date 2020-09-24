import os

import pandas as pd
import pytest

from miner.message.conversation import Conversation


@pytest.fixture(scope="session")
def convo():
    return Conversation(
        path=f"{os.getcwd()}/test_data/messages/inbox/tokehal_sdf7fs9d876/message_1.json"
    )


def test_data_is_df(convo):
    assert isinstance(convo.data, pd.DataFrame)


def test_df_shape(convo):
    assert convo.data.shape == (5, 4)


def test_data_has_right_length(convo):
    assert len(convo.data) == 5


def test_metadata_has_fields(convo):
    expected_fields = [
        "is_still_participant",
        "media_dir",
        "participants",
        "thread_path",
        "thread_type",
        "title",
    ]
    for field in expected_fields:
        assert hasattr(convo.metadata, field)


def test_title(convo):
    assert convo.metadata.title == "Tőke Hal"


def test_participants(convo, app):
    assert convo.metadata.participants == ["Tőke Hal", app._config.get("profile").name]


def test_thread_path(convo):
    assert convo.metadata.thread_path == "tokehal_sdf7fs9d876"


def test_media_dir(convo):
    assert convo.metadata.media_dir is None
