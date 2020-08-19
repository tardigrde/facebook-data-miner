import pytest

from miner.ConversationAnalyzer import ConversationAnalyzer
from miner.utils import dt


# @pytest.fixture(scope='session')
# def person(get_people):
#     def _person(name):
#         people = get_people(name)
#         return people.data[name]
#
#     return _person


@pytest.fixture(scope='session')
def analyze(get_people):
    def _analyze(name):
        people = get_people(name)
        return ConversationAnalyzer(people)

    return _analyze


@pytest.fixture(scope='session')
def statistics(analyze):
    def _stats(name, **kwargs):
        analyzer = analyze(name)
        if 'subject' in kwargs or 'start' in kwargs or 'end' in kwargs:  # and others
            return analyzer.get_stats(**kwargs)
        else:
            return analyzer.stats

    return _stats


# TODO LATER or not extend all functions with all the data
def test_stats_toke_hal_all(statistics):
    stats = statistics('Tőke Hal')

    assert stats.msg_count == 5
    assert stats.unique_msg_count == 4
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 6
    assert stats.unique_word_count == 4
    # assert stats.word_frequency == 0
    assert stats.char_count == 17
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_me(statistics):
    stats = statistics('Tőke Hal', subject='me')

    assert stats.msg_count == 3
    assert stats.unique_msg_count == 3
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 4
    assert stats.unique_word_count == 3
    # assert stats.word_frequency == 0
    assert stats.char_count == 12
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner(statistics):
    stats = statistics('Tőke Hal', subject='partner')

    assert stats.msg_count == 2
    assert stats.unique_msg_count == 2
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 2
    assert stats.unique_word_count == 2
    # assert stats.word_frequency == 0
    assert stats.char_count == 5
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_all_2014_11(statistics):
    stats = statistics('Tőke Hal', subject='all', start=dt(2014, 11), period='m')

    assert stats.msg_count == 4
    assert stats.unique_msg_count == 3
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    # assert stats.word_frequency == 0
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_11(statistics):
    stats = statistics('Tőke Hal', subject='partner', start=dt(2014, 11), period='m')
    assert stats.char_count == 5
    assert stats.word_count == 2


def test_stats_toke_hal_me_2014_11(statistics):
    stats = statistics('Tőke Hal', subject='me', start=dt(2014, 11), period='m')
    assert stats.unique_word_count == 3


#
def test_stats_toke_hal_all_2014_12(statistics):
    stats = statistics('Tőke Hal', subject='all', start=dt(2014, 12), period='m')
    assert stats.msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.unique_word_count == 1
    # assert stats.word_frequency == 0
    assert stats.char_count == 3
    # assert stats.most_used_chars == 0


def test_stats_toke_hal_partner_2014_12(statistics):
    stats = statistics('Tőke Hal', subject='partner', start=dt(2014, 12), period='m')
    assert stats.word_count == 0


def test_stats_toke_hal_me_2014_12(statistics):
    stats = statistics('Tőke Hal', subject='me', start=dt(2014, 12), period='m')
    assert stats.unique_msg_count == 1


def test_stats_teflon_musk(statistics):
    stats = statistics('Teflon Musk')
    assert stats.msg_count == 6
    assert stats.unique_msg_count == 2
    # assert stats.most_used_msgs == 0 # TODO LATER should only return the most used or e.g. top10 most used
    # assert stats.msg_frequency == 0
    assert stats.word_count == 14
    assert stats.unique_word_count == 7
    # assert stats.word_frequency == 0
    assert stats.char_count == 52  # 23
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_me(statistics):
    stats = statistics('Teflon Musk', subject='me')
    assert stats.msg_count == 3
    assert stats.unique_msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 12
    assert stats.unique_word_count == 6
    # assert stats.word_frequency == 0
    assert stats.char_count == 48
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_partner(statistics):
    stats = statistics('Teflon Musk', subject='partner')
    assert stats.msg_count == 3
    assert stats.unique_msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 2
    assert stats.unique_word_count == 1
    # assert stats.word_frequency == 0
    assert stats.char_count == 4
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_all_2014_9(statistics):
    stats = statistics('Teflon Musk', subject='all', start=dt(2014, 9), period='m')
    assert stats.msg_count == 1
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 6
    # assert stats.word_frequency == 0
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_me_2014_9(statistics):
    stats = statistics('Teflon Musk', subject='me', start=dt(2014, 9), period='m')
    assert stats.unique_word_count == 6


def test_stats_teflon_musk_partner_2014_9(statistics):
    stats = statistics('Teflon Musk', subject='partner', start=dt(2014, 9), period='m')
    assert stats.unique_msg_count == 0
    assert stats.char_count == 0


def test_stats_teflon_musk_all_2014_11(statistics):
    stats = statistics('Teflon Musk', subject='all', start=dt(2014, 11), period='m')
    assert stats.msg_count == 4
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    # assert stats.word_frequency == 0
    # assert stats.most_used_chars == 0


def test_stats_teflon_musk_me_2014_11(statistics):
    stats = statistics('Teflon Musk', subject='me', start=dt(2014, 11), period='m')
    assert stats.word_count == 6


def test_stats_teflon_musk_partner_2014_11(statistics):
    stats = statistics('Teflon Musk', subject='partner', start=dt(2014, 11), period='m')
    assert stats.unique_msg_count == 1
    assert stats.unique_word_count == 1
    assert stats.char_count == 4


def test_stats_teflon_musk_all_2014_12(statistics):
    stats = statistics('Teflon Musk', subject='all', start=dt(2014, 12), period='m')

    assert stats.msg_count == 1
    assert stats.unique_msg_count == 0
    # assert stats.most_used_msgs == 0
    # assert stats.msg_frequency == 0
    assert stats.word_count == 0
    assert stats.unique_word_count == 0
    # assert stats.word_frequency == 0
    assert stats.char_count == 0
    # assert stats.most_used_chars == 0



