import pandas as pd
import pytest
from miner.Conversations import Conversations
from miner import utils
import os
TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


@pytest.fixture()
def convos():
    convo = Conversations(f'{TEST_DATA_PATH}')
    return convo.get_people_from_private_messages()


def test_get_all_people_from_convo(convos):
    people = []
    # TODO make this work
    for convo in convos.keys():
        if convo.startswith('group'):
            people += [p for p in convos[convo].get('participants')]
        else:
            people.append(convo)
    people = list(set(people))

    expected = ['Dér Dénes', 'Facebook User', 'Foo Bar', 'John Doe', 'Teflon Musk', 'Benedek Elek', 'Donald Duck',
                'Tőke Hal']
    # TODO LATER what to do with Facebook User??????
    assert sorted(people) == sorted(expected)


def test_all_convos_have_dir(convos):
    assert all([data.messages_dir for data in convos.values()])


def test_all_convos_have_messages_df(convos):
    assert all([isinstance(data.messages, pd.DataFrame) for data in convos.values()])


def test_some_convos_as_media_dir(convos):
    assert convos.get('Teflon Musk').media_dir
    assert not convos.get('Benedek Elek').media_dir

def test_convo_media_has_one_folder_of_possibles(convos):
    listed_dir = os.listdir(f"{TEST_DATA_PATH}/{utils.MESSAGE_SUBPATH}/{convos.get('Teflon Musk').media_dir}")
    assert 'files' in listed_dir
    assert 'photos' in listed_dir
    assert 'audio' not in listed_dir

def test_groups_have_more_than_two_participates(convos):
    groups = {convo: data for convo, data in convos.items() if convo.startswith('group')}
    # TODO participants should contain the user itself as well
    assert all([len(data.get('participants')) > 2 for data in groups.values()])



"""
testcases:
- individual convos contain all names, compact_names, message folders and media folders
  - media folders are a big question. how do you get it? actually once you have the thread_path then from that you can guess,
  OR better off use the uri in the messages... fuck seems complicated
- friends contain all names and compact names,
- convos and friends has a common set, and the set is identical
- people gets assigned with all the unique friends and individual/group convos

gonna test:
- assigning messages to friends,
- deal with multiple directories, IF there are multiple directories,
- 
concerns:
- what to do with non-friends,
- I assume multiple directories are because of files sent,
"""
