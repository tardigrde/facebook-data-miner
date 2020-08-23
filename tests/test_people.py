import pytest
import os
import pandas as pd

from miner.person import Person
from miner import utils

TEST_DATA_PATH = f'{os.getcwd()}/test_data'


@pytest.fixture()
def people_names():
    return ['John Doe', 'Donald Duck', 'Szett Droxler', 'Foo Bar', 'Tőke Hal', 'Dér Dénes', 'Teflon Musk', 'Daisy Duck',
            'Guy Fawkes', 'Benedek Elek']


@pytest.fixture
def people(get_people):
    return get_people()


def test_people_name(people, people_names):
    people_without_groups = [p for p in people.data.keys() if not p.startswith('group')]
    assert sorted(people_names) == sorted(people_without_groups)


def test_some_convos_are_with_friends(people):
    assert people.data.get('Teflon Musk').friend
    assert not people.data.get('Benedek Elek').friend


def test_specific_people_has_or_has_not_got_messages(people):
    assert isinstance(people.data.get('Benedek Elek').messages, pd.DataFrame)
    assert len(people.data.get('Benedek Elek').messages)

    assert isinstance(people.data.get('Teflon Musk').messages, pd.DataFrame)
    assert len(people.data.get('Teflon Musk').messages)

    assert isinstance(people.data.get('John Doe').messages, pd.DataFrame)
    assert not len(people.data.get('John Doe').messages)

    assert isinstance(people.data.get('Szett Droxler').messages, pd.DataFrame)
    assert not len(people.data.get('Szett Droxler').messages)


def test_people_are_individual_instances(people):
    assert all([isinstance(person, Person) for person in people.data.values()])


def test_all_individual_have_messages_df(people):
    assert all([isinstance(person.messages, pd.DataFrame) for person in people.data.values()])


def test_some_individual_have_thread_path(people):
    assert any([person.thread_path for person in people.data.values()])


def test_some_individual_as_media_dir(people):
    assert people.data.get('Teflon Musk').media_dir
    assert not people.data.get('Benedek Elek').media_dir


def test_individual_media_has_one_folder_of_possibles(people):
    listed_dir = os.listdir(
        f"{TEST_DATA_PATH}/{utils.MESSAGE_SUBPATH}/{people.data.get('Teflon Musk').media_dir}")
    assert 'files' in listed_dir
    assert 'photos' in listed_dir
    assert 'audio' not in listed_dir


