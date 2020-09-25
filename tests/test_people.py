import os

import pandas as pd
import pytest

from miner.person import Person
from miner.utils import const


@pytest.fixture()
def people_names():
    return [
        "John Doe",
        "Donald Duck",
        "Szett Droxler",
        "Foo Bar",
        "Tőke Hal",
        "Dér Dénes",
        "Facebook User",
        "Jenő Rejtő",
        "Bugs Bunny",
        "Daisy Duck",
        "Guy Fawkes",
        "Benedek Elek",
    ]


def test_people_name(people, people_names):
    people = [p for p in people.data.keys()]
    assert sorted(people_names) == sorted(people)


def test_some_convos_are_with_friends(people):
    assert people.data.get("Bugs Bunny").friend
    assert not people.data.get("Benedek Elek").friend


def test_messages_are_df(people):
    assert all(
        [isinstance(person.messages, pd.DataFrame) for person in people.data.values()]
    )


def test_specific_people_has_or_has_not_got_messages(people):
    assert isinstance(people.data.get("Benedek Elek").messages, pd.DataFrame)
    assert len(people.data.get("Benedek Elek").messages)

    assert isinstance(people.data.get("Bugs Bunny").messages, pd.DataFrame)
    assert len(people.data.get("Bugs Bunny").messages)

    assert isinstance(people.data.get("John Doe").messages, pd.DataFrame)
    assert not len(people.data.get("John Doe").messages)

    assert isinstance(people.data.get("Szett Droxler").messages, pd.DataFrame)
    assert not len(people.data.get("Szett Droxler").messages)


def test_people_are_Person_instances(people):
    assert all([isinstance(person, Person) for person in people.data.values()])


def test_some_have_thread_path(people):
    assert any([person.thread_path for person in people.data.values()])


def test_some_as_media_dir(people):
    assert people.data.get("Bugs Bunny").media_dir
    assert not people.data.get("Benedek Elek").media_dir


def test_media_has_one_folder_of_possibles(people):
    listed_dir = os.listdir(
        f"{os.getcwd()}/test_data/{const.MESSAGE_SUBPATH}/{people.data.get('Bugs Bunny').media_dir}"
    )
    assert "files" in listed_dir
    assert "photos" in listed_dir
    assert "audio" not in listed_dir
