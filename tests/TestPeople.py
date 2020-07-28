import pytest
from People import People


@pytest.fixture()
def people():
    # TODO solve paths
    p = People(path='/home/levente/projects/facebook-data-miner/tests/test_data')
    p.to_individuals()
    return p


@pytest.fixture()
def people_names():
    return ['John Doe', 'Donald Duck', 'Szett Droxler', 'Foo Bar', 'Tőke Hal', 'Dér Dénes', 'Teflon Musk', 'Daisy Duck',
            'Guy Fawkes', 'Benedek Elek']


def test_specific_people_has_or_has_not_got_messages(people):
    # TODO parametrize
    import pandas as pd
    assert isinstance(people.data.get('Benedek Elek').get('messages'), pd.DataFrame)
    assert isinstance(people.data.get('Teflon Musk').get('messages'), pd.DataFrame)
    assert isinstance(people.data.get('Tőke Hal').get('messages'), pd.DataFrame)
    assert not isinstance(people.data.get('John Doe').get('messages'), pd.DataFrame)
    assert not isinstance(people.data.get('Szett Droxler').get('messages'), pd.DataFrame)
    assert not isinstance(people.data.get('Daisy Duck').get('messages'), pd.DataFrame)
    assert not isinstance(people.data.get('Guy Fawkes').get('messages'), pd.DataFrame)


def test_people_name(people, people_names):
    people_without_groups = [p for p in people.data.keys() if not p.startswith('group')]
    assert sorted(people_names) == sorted(people_without_groups)


def test_some_convos_are_with_friends(people):
    assert people.data.get('Teflon Musk').get('friend')
    assert not people.data.get('Benedek Elek').get('friend')


def test_specific_people_has_or_has_not_got_media(people):
    assert people.data.get('Teflon Musk').get('media_dir')

#TODO test individuals too