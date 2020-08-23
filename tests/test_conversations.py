import pytest
from miner.message.conversations import Conversations
from miner.message.conversation import Conversation
from miner import utils

import os

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


def test_if_convos_has_correct_length(conversations):
    assert len(conversations.private) == 4
    assert len(conversations.group) == 3


def test_private_has_conversation_instances(conversations):
    for convo in conversations.private.values():
        assert isinstance(convo, Conversation)
    for convo in conversations.group.values():
        assert isinstance(convo, Conversation)


def test_specific_people_has_got_media(conversations):
    assert conversations.private.get('Teflon Musk').metadata.media_dir == 'TeflonMusk_fSD454F'


def test_get_all_people_from_private_messages(conversations):
    people = list(conversations.private.keys())
    expected = ['Foo Bar', 'Teflon Musk', 'Benedek Elek', 'Tőke Hal']
    assert sorted(people) == sorted(expected)


def test_get_all_people_from_convo(conversations):
    people = []
    # indie
    people += list(conversations.private.keys())
    # group
    people_from_groups = [p for convo in conversations.group.values() for p in convo.metadata.participants]

    people += people_from_groups

    expected = ['Dér Dénes', 'Facebook User', 'Foo Bar', 'John Doe', utils.ME, 'Teflon Musk', 'Benedek Elek',
                'Donald Duck', 'Tőke Hal']

    assert sorted(list(set(people))) == sorted(expected)


def test_groups_have_more_than_two_participates(conversations):
    assert all([len(data.metadata.participants) > 2 for data in conversations.group.values()])



# TODO remove private convo jsons after every test