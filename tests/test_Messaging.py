import pytest
from miner.Messaging import Messaging
from miner.Conversation import Conversation

from miner import utils
import os

TEST_DATA_PATH = f'{os.getcwd()}/test_data'



def test_if_paths_are_registered(conversations):
    assert len(conversations.directories.private) == 4
    assert len(conversations.directories.group) == 3


def test_if_convos_has_correct_length(conversations):
    assert len(conversations.private) == 4
    assert len(conversations.group) == 3


def test_private_has_conversation_instances(conversations):
    for convo in conversations.private.values():
        assert isinstance(convo, Conversation)
    for convo in conversations.group.values():
        assert isinstance(convo, Conversation)

# def test_get_all_people_from_private_messages(people_from_private_convos):
#     people = list(people_from_private_convos.keys())
#     expected = ['Foo Bar', 'Teflon Musk', 'Benedek Elek', 'Tőke Hal']
#     assert sorted(people) == sorted(expected)


# def test_get_all_people_from_convo(conversations):
#     people = []
#     # indie
#     people += list(conversations.private_convo_paths.keys())
#     # group
#     people_from_groups = [p for people in conversations.group_convo_paths.values() for p in people]
#
#     people += people_from_groups
#
#     expected = ['Dér Dénes', 'Facebook User', 'Foo Bar', 'John Doe', 'Teflon Musk', 'Benedek Elek', 'Donald Duck',
#                 'Tőke Hal']
#
#     assert sorted(list(set(people))) == sorted(expected)


# def test_people_are_individual_instances(people_from_private_convos):
#     assert all([isinstance(person, Person) for person in people_from_private_convos.values()])


# def test_all_individual_have_messages_df(people_from_private_convos):
#     assert all([isinstance(data.messages, pd.DataFrame) for data in people_from_private_convos.values()])


# def test_all_individual_have_dir(people_from_private_convos):
#     assert all([data.messages_dir for data in people_from_private_convos.values()])


# def test_some_individual_as_media_dir(people_from_private_convos):
#     assert people_from_private_convos.get('Teflon Musk').media_dir
#     assert not people_from_private_convos.get('Benedek Elek').media_dir


# def test_individual_media_has_one_folder_of_possibles(people_from_private_convos):
#     listed_dir = os.listdir(
#         f"{TEST_DATA_PATH}/{utils.MESSAGE_SUBPATH}/{people_from_private_convos.get('Teflon Musk').media_dir}")
#     assert 'files' in listed_dir
#     assert 'photos' in listed_dir
#     assert 'audio' not in listed_dir


# def test_groups_have_more_than_two_participates(people_from_private_convos):
#     groups = {convo: data for convo, data in people_from_private_convos.items() if convo.startswith('group')}
#     assert all([len(data.get('participants')) > 2 for data in groups.values()])
