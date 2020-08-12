import pytest

from miner.Friends import Friends

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


@pytest.fixture()
def expected_friends():
    return {'John Doe': {'compact_name': 'johndoe', 'path': None},
            'Donald Duck': {'compact_name': 'donaldduck', 'path': None},
            'Szett Droxler': {'compact_name': 'szettdroxler', 'path': None},
            'Foo Bar': {'compact_name': 'foobar', 'path': None},
            'Tőke Hal': {'compact_name': 'tokehal', 'path': None},
            'Dér Dénes': {'compact_name': 'derdenes', 'path': None},
            'Teflon Musk': {'compact_name': 'teflonmusk', 'path': None},
            'Daisy Duck': {'compact_name': 'daisyduck', 'path': None},
            'Guy Fawkes': {'compact_name': 'guyfawkes', 'path': None}}


@pytest.fixture()
def friends():
    f = Friends(f'{TEST_DATA_PATH}/friends/friends.json')
    return f.get_people()


def test_get_peoples_names_from_friends(friends, expected_friends):
    assert all([p in expected_friends.keys() for p in friends])


def test_get_peoples_compact_name_from_friends(friends, expected_friends):
    expected_compact_names = [value.get('compact_name') for value in expected_friends.values()]

    assert all([p.compact_name in expected_compact_names for p in friends.values()])



# TODO what happens when two friends have same name??
