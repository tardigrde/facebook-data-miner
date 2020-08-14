import pandas as pd
import pytest
from miner.Conversations import Conversations
from miner.Individual import Individual
from miner import utils
import os

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


@pytest.fixture()
def conversations():
    return Conversations(f'{TEST_DATA_PATH}')


@pytest.fixture
def people_from_private_convos(conversations):
    return conversations.get_people_from_private_messages()


def test_if_paths_are_registered(conversations):
    assert len(conversations.private_convo_paths) == 4
    assert len(conversations.group_convo_paths) == 3
    assert len(conversations.deleted_user_convo_paths) == 0


def test_get_all_people_from_private_messages(people_from_private_convos):
    people = list(people_from_private_convos.keys())
    expected = ['Foo Bar', 'Teflon Musk', 'Benedek Elek', 'Tőke Hal']
    assert sorted(people) == sorted(expected)


def test_get_all_people_from_convo(conversations):
    people = []
    # indie
    people += list(conversations.private_convo_paths.keys())
    # group
    people_from_groups = [p for people in conversations.group_convo_paths.values() for p in people]

    people += people_from_groups

    expected = ['Dér Dénes', 'Facebook User', 'Foo Bar', 'John Doe', 'Teflon Musk', 'Benedek Elek', 'Donald Duck',
                'Tőke Hal']

    assert sorted(list(set(people))) == sorted(expected)


def test_people_are_individual_instances(people_from_private_convos):
    assert all([isinstance(person, Individual) for person in people_from_private_convos.values()])


def test_all_individual_have_messages_df(people_from_private_convos):
    assert all([isinstance(data.messages, pd.DataFrame) for data in people_from_private_convos.values()])


def test_all_individual_have_dir(people_from_private_convos):
    assert all([data.messages_dir for data in people_from_private_convos.values()])


def test_some_individual_as_media_dir(people_from_private_convos):
    assert people_from_private_convos.get('Teflon Musk').media_dir
    assert not people_from_private_convos.get('Benedek Elek').media_dir


def test_individual_media_has_one_folder_of_possibles(people_from_private_convos):
    listed_dir = os.listdir(
        f"{TEST_DATA_PATH}/{utils.MESSAGE_SUBPATH}/{people_from_private_convos.get('Teflon Musk').media_dir}")
    assert 'files' in listed_dir
    assert 'photos' in listed_dir
    assert 'audio' not in listed_dir


def test_groups_have_more_than_two_participates(people_from_private_convos):
    groups = {convo: data for convo, data in people_from_private_convos.items() if convo.startswith('group')}
    # TODO participants should contain the user itself as well
    assert all([len(data.get('participants')) > 2 for data in groups.values()])
