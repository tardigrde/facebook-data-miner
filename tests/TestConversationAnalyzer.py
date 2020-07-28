import pandas as pd
import pytest
from ConversationAnalyzer import ConversationAnalyzer
from Conversations import Messages
from People import People
import os

TEST_DATA_PATH = '/home/levente/projects/facebook-data-miner/tests/test_data'


@pytest.fixture()
def person_Toke_Hal():
    p = People(path='/home/levente/projects/facebook-data-miner/tests/test_data')
    p.to_individuals()
    for person in p.individuals:
        if person.name == 'Tőke Hal':
            return person


@pytest.fixture()
def person_Teflon_Musk():
    p = People(path='/home/levente/projects/facebook-data-miner/tests/test_data')
    p.to_individuals()
    for person in p.individuals:
        if person.name == 'Teflon Musk':
            return person


def test_stats_toke_hal(person_Toke_Hal):
    analyzer = ConversationAnalyzer(person_Toke_Hal.name, person_Toke_Hal.messages)
    stats = analyzer.stats

    assert stats.get('all').msg_count == 5
    assert stats.get('all').unique_msg_count == 4
    # assert stats.get('all').most_used_msgs == 0
    # assert stats.get('all').msg_frequency == 0
    assert stats.get('all').word_count == 6
    assert stats.get('all').unique_word_count == 4
    # assert stats.get('all').word_frequency == 0
    assert stats.get('all').char_count == 17
    # assert stats.get('all').most_used_chars == 0

    assert stats.get('me').msg_count == 3
    assert stats.get('me').unique_msg_count == 3
    # assert stats.get('me').most_used_msgs == 0
    # assert stats.get('me').msg_frequency == 0
    assert stats.get('me').word_count == 4
    assert stats.get('me').unique_word_count == 3
    # assert stats.get('me').word_frequency == 0
    assert stats.get('me').char_count == 12
    # assert stats.get('me').most_used_chars == 0

    assert stats.get('partner').msg_count == 2
    assert stats.get('partner').unique_msg_count == 2
    # assert stats.get('partner').most_used_msgs == 0
    # assert stats.get('partner').msg_frequency == 0
    assert stats.get('partner').word_count == 2
    assert stats.get('partner').unique_word_count == 2
    # assert stats.get('partner').word_frequency == 0
    assert stats.get('partner').char_count == 5
    # assert stats.get('partner').most_used_chars == 0

    assert stats.get('grouped').get(2014).get(11).get('all').msg_count == 4
    assert stats.get('grouped').get(2014).get(11).get('all').unique_msg_count == 3
    # assert stats.get('grouped').get(2014).get(11).get('all').most_used_msgs == 0
    # assert stats.get('grouped').get(2014).get(11).get('all').msg_frequency == 0
    assert stats.get('grouped').get(2014).get(11).get('partner').word_count == 2
    assert stats.get('grouped').get(2014).get(11).get('me').unique_word_count == 3
    # assert stats.get('grouped').get(2014).get(11).get('all').word_frequency == 0
    assert stats.get('grouped').get(2014).get(11).get('partner').char_count == 5
    # assert stats.get('grouped').get(2014).get(11).get('all').most_used_chars == 0

    assert stats.get('grouped').get(2014).get(12).get('all').msg_count == 1
    assert stats.get('grouped').get(2014).get(12).get('me').unique_msg_count == 1
    # assert stats.get('grouped').get(2014).get(12).get('all').most_used_msgs == 0
    # assert stats.get('grouped').get(2014).get(12).get('all').msg_frequency == 0
    assert stats.get('grouped').get(2014).get(12).get('partner').word_count == 0
    assert stats.get('grouped').get(2014).get(12).get('all').unique_word_count == 1
    # assert stats.get('grouped').get(2014).get(12).get('all').word_frequency == 0
    assert stats.get('grouped').get(2014).get(12).get('all').char_count == 3
    # assert stats.get('grouped').get(2014).get(12).get('all').most_used_chars == 0


def test_stats_teflon_musk(person_Teflon_Musk):
    analyzer = ConversationAnalyzer(person_Teflon_Musk.name, person_Teflon_Musk.messages)
    stats = analyzer.stats

    assert stats.get('all').msg_count == 6
    assert stats.get('all').unique_msg_count == 2  # TODO this does not count media messages
    # assert stats.get('all').most_used_msgs == 0 # TODO should only return the most used or e.g. top10 most used
    # assert stats.get('all').msg_frequency == 0
    assert stats.get('all').word_count == 14
    assert stats.get('all').unique_word_count == 7
    # assert stats.get('all').word_frequency == 0
    assert stats.get('all').char_count == 52  # 23
    # assert stats.get('all').most_used_chars == 0

    assert stats.get('me').msg_count == 3
    assert stats.get('me').unique_msg_count == 1
    # assert stats.get('me').most_used_msgs == 0
    # assert stats.get('me').msg_frequency == 0
    assert stats.get('me').word_count == 12
    assert stats.get('me').unique_word_count == 6
    # assert stats.get('me').word_frequency == 0
    assert stats.get('me').char_count == 48
    # assert stats.get('me').most_used_chars == 0

    assert stats.get('partner').msg_count == 3
    assert stats.get('partner').unique_msg_count == 1
    # assert stats.get('partner').most_used_msgs == 0
    # assert stats.get('partner').msg_frequency == 0
    assert stats.get('partner').word_count == 2
    assert stats.get('partner').unique_word_count == 1
    # assert stats.get('partner').word_frequency == 0
    assert stats.get('partner').char_count == 4
    # assert stats.get('partner').most_used_chars == 0

    assert stats.get('grouped').get(2014).get(9).get('all').msg_count == 1
    assert stats.get('grouped').get(2014).get(9).get('partner').unique_msg_count == 0
    # assert stats.get('grouped').get(2014).get(9).get('all').most_used_msgs == 0
    # assert stats.get('grouped').get(2014).get(9).get('all').msg_frequency == 0
    assert stats.get('grouped').get(2014).get(9).get('all').word_count == 6
    assert stats.get('grouped').get(2014).get(9).get('me').unique_word_count == 6
    # assert stats.get('grouped').get(2014).get(9).get('all').word_frequency == 0
    assert stats.get('grouped').get(2014).get(9).get('partner').char_count == 0
    # assert stats.get('grouped').get(2014).get(9).get('all').most_used_chars == 0

    assert stats.get('grouped').get(2014).get(11).get('all').msg_count == 4
    assert stats.get('grouped').get(2014).get(11).get('partner').unique_msg_count == 1
    # assert stats.get('grouped').get(2014).get(11).get('all').most_used_msgs == 0
    # assert stats.get('grouped').get(2014).get(11).get('all').msg_frequency == 0
    assert stats.get('grouped').get(2014).get(11).get('me').word_count == 6
    assert stats.get('grouped').get(2014).get(11).get('partner').unique_word_count == 1
    # assert stats.get('grouped').get(2014).get(11).get('all').word_frequency == 0
    assert stats.get('grouped').get(2014).get(11).get('partner').char_count == 4
    # assert stats.get('grouped').get(2014).get(11).get('all').most_used_chars == 0

    assert stats.get('grouped').get(2014).get(12).get('all').msg_count == 1
    assert stats.get('grouped').get(2014).get(12).get('all').unique_msg_count == 0
    # assert stats.get('grouped').get(2014).get(12).get('all').most_used_msgs == 0
    # assert stats.get('grouped').get(2014).get(12).get('all').msg_frequency == 0
    assert stats.get('grouped').get(2014).get(12).get('all').word_count == 0
    assert stats.get('grouped').get(2014).get(12).get('all').unique_word_count == 0
    # assert stats.get('grouped').get(2014).get(12).get('all').word_frequency == 0
    assert stats.get('grouped').get(2014).get(12).get('all').char_count == 0
    # assert stats.get('grouped').get(2014).get(12).get('all').most_used_chars == 0
