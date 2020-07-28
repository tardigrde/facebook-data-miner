import pytest

from Friends import Friends

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


@pytest.fixture()
def friends():
    return {'John Doe': {'compact_name': 'johndoe', 'path': None},
            'Donald Duck': {'compact_name': 'donaldduck', 'path': None},
            'Szett Droxler': {'compact_name': 'szettdroxler', 'path': None},
            'Foo Bar': {'compact_name': 'foobar', 'path': None},
            'Tőke Hal': {'compact_name': 'tokehal', 'path': None},
            'Dér Dénes': {'compact_name': 'derdenes', 'path': None},
            'Teflon Musk': {'compact_name': 'teflonmusk', 'path': None},
            'Daisy Duck': {'compact_name': 'daisyduck', 'path': None},
            'Guy Fawkes': {'compact_name': 'guyfawkes', 'path': None}}


def test_get_peoples_names_from_friends(friends):
    # TODO refactor this two lines into a fixture
    f = Friends(f'{TEST_DATA_PATH}/friends/friends.json')
    people = f.get_people()

    expected_people = friends.keys()

    assert all([p in expected_people for p in people])


def test_get_peoples_compact_name_from_friends(friends):
    f = Friends(f'{TEST_DATA_PATH}/friends/friends.json')
    people = f.get_people()

    expected_compact_names = [value.get('compact_name') for value in friends.values()]

    assert all([p.get('compact_name') in expected_compact_names for p in people.values()])

# TODO what happens when two friends have same name??

